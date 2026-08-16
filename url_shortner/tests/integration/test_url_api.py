import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_short_url(client: AsyncClient):
    payload = {"original_url": "https://example.com/item/100"}
    response = await client.post("/api/v1/urls", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://example.com/item/100"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_custom_alias(client: AsyncClient):
    payload = {
        "original_url": "https://example.com/promo",
        "custom_alias": "special-offer",
    }
    response = await client.post("/api/v1/urls", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["short_code"] == "special-offer"


@pytest.mark.asyncio
async def test_custom_alias_conflict(client: AsyncClient):
    payload = {
        "original_url": "https://example.com/promo1",
        "custom_alias": "dup-alias",
    }
    res1 = await client.post("/api/v1/urls", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/urls", json=payload)
    assert res2.status_code == 409
    assert "already taken" in res2.json()["detail"]


@pytest.mark.asyncio
async def test_redirect_to_url(client: AsyncClient):
    create_res = await client.post(
        "/api/v1/urls",
        json={"original_url": "https://target-destination.com/page"},
    )
    assert create_res.status_code == 201
    short_code = create_res.json()["short_code"]

    redirect_res = await client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["location"] == "https://target-destination.com/page"


@pytest.mark.asyncio
async def test_analytics(client: AsyncClient):
    create_res = await client.post(
        "/api/v1/urls",
        json={
            "original_url": "https://analytics-test.com",
            "custom_alias": "analytics-code",
        },
    )
    assert create_res.status_code == 201

    # Simulate 2 clicks
    await client.get("/analytics-code", follow_redirects=False)
    await client.get("/analytics-code", follow_redirects=False)

    analytics_res = await client.get("/api/v1/urls/analytics-code/analytics")
    assert analytics_res.status_code == 200
    data = analytics_res.json()
    assert data["short_code"] == "analytics-code"
    assert data["total_clicks"] == 2


@pytest.mark.asyncio
async def test_delete_url(client: AsyncClient):
    create_res = await client.post(
        "/api/v1/urls",
        json={
            "original_url": "https://to-be-deleted.com",
            "custom_alias": "delete-me",
        },
    )
    assert create_res.status_code == 201

    del_res = await client.delete("/api/v1/urls/delete-me")
    assert del_res.status_code == 204

    # Redirect should now return 404
    get_res = await client.get("/delete-me", follow_redirects=False)
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_non_existent_url(client: AsyncClient):
    res = await client.get("/nonexistent123", follow_redirects=False)
    assert res.status_code == 404
