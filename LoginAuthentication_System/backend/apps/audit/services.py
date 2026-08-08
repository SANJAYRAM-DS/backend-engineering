from typing import Optional, Dict, Any
from apps.users.models import User
from apps.audit.models import AuditLog

class AuditService:
    @staticmethod
    def log_event(
        user: Optional[User],
        event_type: str,
        ip_address: str,
        user_agent: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Create an immutable security audit log record."""
        return AuditLog.objects.create(
            user=user,
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent or "Unknown",
            status=status,
            details=details or {}
        )
