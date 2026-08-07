# Phase 31: Comprehensive Pytest & Security Test Suite

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 31 of 35  
> **Target Path**: `docs/31-testing.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Building an isolated Pytest fixture hierarchy using `@pytest.fixture`.
* Testing cryptographic time expiry using `freezegun`.
* Writing unit, integration, and security edge-case test suites.

---

## 2. Code Implementation & Steps

### Step 1: Pytest Setup & Fixtures (`tests/conftest.py`)

File path: `tests/conftest.py`

```python
"""
Pytest Test Fixture Suite.
Configures database isolation and reusable test user objects.
"""
import pytest
from apps.users.models import User

@pytest.fixture
def db_user(db) -> User:
    """Fixture returning an active verified test user."""
    return User.objects.create_user(
        email="testuser@example.com",
        password="P@ssw0rd12345!",
        first_name="Test",
        last_name="User",
        is_email_verified=True,
    )
```

### Step 2: Authentication Unit Test (`tests/unit/test_authentication.py`)

File path: `tests/unit/test_authentication.py`

```python
"""
Authentication & JWT Unit Test Suite.
"""
import pytest
from apps.authentication.services import AuthenticationService
from apps.authentication.jwt import JWTService
from core.exceptions import AuthenticationError

@pytest.mark.django_db
def test_successful_authentication(db_user):
    user = AuthenticationService.authenticate_credentials("testuser@example.com", "P@ssw0rd12345!")
    assert user.id == db_user.id

@pytest.mark.django_db
def test_invalid_password_raises_authentication_error(db_user):
    with pytest.raises(AuthenticationError):
        AuthenticationService.authenticate_credentials("testuser@example.com", "WrongPassword123!")

def test_jwt_generation_and_decoding():
    token = JWTService.create_access_token(user_id="test-uuid-123", email="user@test.com")
    payload = JWTService.decode_token(token)
    assert payload["sub"] == "test-uuid-123"
    assert payload["email"] == "user@test.com"
```

---

## 3. Mentor Mode: Self-Check

### Self-Check Questions
1. Why is `@pytest.mark.django_db` necessary for tests that interact with models?  
   *Answer: It wraps the test inside an isolated database transaction, rolling back changes after the test completes so tests do not pollute each other.*
