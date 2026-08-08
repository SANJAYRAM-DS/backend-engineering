import pytest
from core.security.tokens import create_access_token, decode_access_token
from core.security.crypto import hash_token, verify_password, hash_password

def test_password_hashing():
    pwd = "MySecretPassword123!"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_access_token_creation_and_decoding():
    user_id = "12345678-1234-5678-1234-567812345678"
    email = "user@test.com"
    roles = ["User", "Admin"]
    token, jti = create_access_token(user_id=user_id, email=email, roles=roles)
    
    payload = decode_access_token(token)
    assert payload["sub"] == user_id
    assert payload["email"] == email
    assert payload["roles"] == roles
    assert payload["jti"] == jti
