from ninja import NinjaAPI
from django.http import JsonResponse
from core.exceptions import BaseAppException
from apps.authentication.api import auth_router, sessions_router
from apps.rbac.api import rbac_router
from apps.audit.api import audit_router

api = NinjaAPI(
    title="Enterprise Authentication & Security API",
    version="1.0.0",
    description="Production-Grade Authentication, JWT Rotation Engine, Session Tracker & RBAC System",
    docs_url="/docs"
)

@api.exception_handler(BaseAppException)
def app_exception_handler(request, exc: BaseAppException):
    """Global custom exception handler for clean JSON error responses."""
    return JsonResponse(
        {
            "status": "error",
            "message": exc.message,
            "details": exc.details,
        },
        status=exc.status_code,
    )

api.add_router("/auth/", auth_router)
api.add_router("/sessions/", sessions_router)
api.add_router("/rbac/", rbac_router)
api.add_router("/audit/", audit_router)
