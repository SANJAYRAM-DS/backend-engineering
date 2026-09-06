import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_project_crud_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        dummy_owner_id = str(uuid.uuid4())

        # 1. CREATE Project (POST)
        create_payload = {
            "name": "Test Project",
            "description": "Integration test project",
            "visibility": "PUBLIC",
            "owner_id": dummy_owner_id
        }
        res = await ac.post("/api/v1/projects", json=create_payload)
        assert res.status_code == 201
        data = res.json()
        project_id = data["id"]
        assert data["name"] == "Test Project"

        # 2. GET Project by ID
        res = await ac.get(f"/api/v1/projects/{project_id}")
        assert res.status_code == 200
        assert res.json()["id"] == project_id

        # 3. LIST Projects (GET - Paginated Response)
        res = await ac.get("/api/v1/projects?page=1&limit=10")
        assert res.status_code == 200
        response_json = res.json()
        assert "items" in response_json
        assert "meta" in response_json
        assert isinstance(response_json["items"], list)
        assert response_json["meta"]["page"] == 1

        # 4. UPDATE Project (PUT)
        update_payload = {"name": "Updated Test Project", "visibility": "PRIVATE"}
        res = await ac.put(f"/api/v1/projects/{project_id}", json=update_payload)
        assert res.status_code == 200
        assert res.json()["name"] == "Updated Test Project"
        assert res.json()["visibility"] == "PRIVATE"

        # 5. DELETE Project
        res = await ac.delete(f"/api/v1/projects/{project_id}")
        assert res.status_code == 204

        # 6. Verify 404 NOT FOUND after deletion
        res = await ac.get(f"/api/v1/projects/{project_id}")
        assert res.status_code == 404
