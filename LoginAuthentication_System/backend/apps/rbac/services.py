from apps.users.models import User
from apps.rbac.models import Role, Permission, UserRole
from core.exceptions import NotFoundError

class RbacService:
    @staticmethod
    def user_has_permission(user: User, permission_code: str) -> bool:
        """Check if user has a specific permission code across all assigned roles."""
        if user.is_superuser:
            return True
        return UserRole.objects.filter(
            user=user,
            role__permissions__code=permission_code
        ).exists()

    @staticmethod
    def get_user_permissions(user: User) -> list[str]:
        if user.is_superuser:
            return list(Permission.objects.values_list("code", flat=True))
        return list(
            Permission.objects.filter(roles__userrole__user=user).values_list("code", flat=True).distinct()
        )

    @staticmethod
    def assign_role(user: User, role_name: str) -> UserRole:
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise NotFoundError(f"Role '{role_name}' not found.")
        
        user_role, _ = UserRole.objects.get_or_create(user=user, role=role)
        return user_role

    @staticmethod
    def seed_initial_rbac():
        """Seed default roles and permissions."""
        p_read_users, _ = Permission.objects.get_or_create(code="users:read", defaults={"description": "View user profiles"})
        p_manage_users, _ = Permission.objects.get_or_create(code="users:manage", defaults={"description": "Manage user accounts"})
        p_read_audit, _ = Permission.objects.get_or_create(code="audit:read", defaults={"description": "View security audit logs"})
        p_admin, _ = Permission.objects.get_or_create(code="admin:full", defaults={"description": "Full administrative access"})

        admin_role, _ = Role.objects.get_or_create(name="Admin", defaults={"description": "System Administrator"})
        user_role, _ = Role.objects.get_or_create(name="User", defaults={"description": "Standard Platform User"})
        auditor_role, _ = Role.objects.get_or_create(name="Auditor", defaults={"description": "Security Auditor"})

        admin_role.permissions.add(p_read_users, p_manage_users, p_read_audit, p_admin)
        user_role.permissions.add(p_read_users)
        auditor_role.permissions.add(p_read_audit)
