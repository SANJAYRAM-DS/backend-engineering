import pytest
from apps.users.models import User
from apps.rbac.services import RbacService

@pytest.fixture
def db_user(db):
    user = User.objects.create_user(
        email="testuser@example.com",
        password="SecurePassword123!",
        first_name="Test",
        last_name="User"
    )
    RbacService.seed_initial_rbac()
    return user
