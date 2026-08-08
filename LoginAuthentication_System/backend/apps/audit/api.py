from typing import List
from ninja import Router
from django.http import HttpRequest
from apps.audit.models import AuditLog
from apps.audit.schemas import AuditLogResponseSchema
from apps.authentication.jwt import JWTAuth
from apps.rbac.services import RbacService
from core.exceptions import PermissionDeniedError

audit_router = Router(tags=["Security Audit Logging"])

@audit_router.get("/logs", auth=JWTAuth(), response={200: List[AuditLogResponseSchema]})
def list_audit_logs(request: HttpRequest):
    """Retrieves immutable security audit log entries."""
    if not request.user.is_superuser and not RbacService.user_has_permission(request.user, "audit:read"):
        raise PermissionDeniedError("Permission 'audit:read' or superuser status required to view audit logs.")
    
    logs = AuditLog.objects.select_related("user").all()[:100]
    return [
        {
            "id": str(log.id),
            "user_id": str(log.user.id) if log.user else None,
            "user_email": log.user.email if log.user else "Anonymous/Unauthenticated",
            "event_type": log.event_type,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "status": log.status,
            "details": log.details,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]
