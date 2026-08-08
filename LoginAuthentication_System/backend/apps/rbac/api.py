from typing import List
from ninja import Router
from django.http import HttpRequest
from apps.rbac.models import Role, Permission
from apps.rbac.schemas import RoleSchema, PermissionSchema, AssignRoleSchema
from apps.rbac.services import RbacService
from apps.authentication.jwt import JWTAuth
from apps.users.models import User
from core.exceptions import PermissionDeniedError, NotFoundError

rbac_router = Router(tags=["Role-Based Access Control (RBAC)"])

@rbac_router.get("/roles", auth=JWTAuth(), response={200: List[RoleSchema]})
def list_roles(request: HttpRequest):
    """Lists all configured RBAC roles and permissions."""
    roles = Role.objects.prefetch_related("permissions").all()
    res = []
    for r in roles:
        perms = [
            {"id": str(p.id), "code": p.code, "description": p.description}
            for p in r.permissions.all()
        ]
        res.append({
            "id": str(r.id),
            "name": r.name,
            "description": r.description,
            "permissions": perms
        })
    return res

@rbac_router.get("/permissions", auth=JWTAuth(), response={200: List[PermissionSchema]})
def list_permissions(request: HttpRequest):
    """Lists all available system permissions."""
    permissions = Permission.objects.all()
    return [
        {"id": str(p.id), "code": p.code, "description": p.description}
        for p in permissions
    ]

@rbac_router.post("/assign-role", auth=JWTAuth(), response={200: dict})
def assign_role(request: HttpRequest, payload: AssignRoleSchema):
    """Assigns an RBAC role to a target user (Requires Admin role or superuser)."""
    if not request.user.is_superuser and not RbacService.user_has_permission(request.user, "admin:full"):
        raise PermissionDeniedError("Admin privileges required to assign roles.")
    
    try:
        target_user = User.objects.get(id=payload.user_id)
    except User.DoesNotExist:
        raise NotFoundError("Target user not found.")
        
    RbacService.assign_role(target_user, payload.role_name)
    return 200, {
        "status": "success",
        "message": f"Role '{payload.role_name}' assigned to user {target_user.email}."
    }
