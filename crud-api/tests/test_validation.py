import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_invalid_create_project_empty_name():
    """Test creating project with an empty string name fails validation."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "name": "",
            "visibility": "PUBLIC",
            "owner_id": str(uuid.uuid4())
        }
        res = await ac.post("/api/v1/projects", json=payload)
        assert res.status_code == 422
        body = res.json()
        assert body["success"] is False
        assert body["error"]["code"] == "VALIDATION_ERROR"
        assert len(body["error"]["details"]) > 0

@pytest.mark.asyncio
async def test_invalid_create_project_bad_visibility():
    """Test creating project with an invalid visibility enum string."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "name": "Valid Name",
            "visibility": "SUPER_SECRET",
            "owner_id": str(uuid.uuid4())
        }
        res = await ac.post("/api/v1/projects", json=payload)
        assert res.status_code == 422
        body = res.json()
        assert body["success"] is False
        assert body["error"]["code"] == "VALIDATION_ERROR"

@pytest.mark.asyncio
async def test_not_found_error_envelope():
    """Test 404 ResourceNotFoundException returns standard error envelope."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        fake_id = str(uuid.uuid4())
        res = await ac.get(f"/api/v1/projects/{fake_id}")
        assert res.status_code == 404
        body = res.json()
        assert body["success"] is False
        assert body["error"]["code"] == "RESOURCE_NOT_FOUND"
        assert f"Project with ID '{fake_id}' was not found." in body["error"]["message"]
