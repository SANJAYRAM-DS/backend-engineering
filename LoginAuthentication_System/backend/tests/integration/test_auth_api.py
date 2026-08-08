import pytest
from django.test import Client

@pytest.mark.django_db
def test_user_registration_and_login_flow():
    client = Client()
    
    # 1. Register User
    reg_payload = {
        "email": "integration@test.com",
        "password": "Password123!",
        "first_name": "Integration",
        "last_name": "Tester"
    }
    response = client.post("/api/v1/auth/register", data=reg_payload, content_type="application/json")
    assert response.status_code == 201
    reg_data = response.json()
    assert reg_data["status"] == "success"
    
    # 2. Login User
    login_payload = {
        "email": "integration@test.com",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/login", data=login_payload, content_type="application/json")
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data

    # 3. Access Protected /me Endpoint
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token_data['access_token']}"}
    me_response = client.get("/api/v1/auth/me", **headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "integration@test.com"
