import uuid
from django.utils import timezone
from apps.users.models import User
from apps.authentication.models import DeviceSession

class SessionService:
    @staticmethod
    def track_session(user: User, ip_address: str, user_agent: str) -> DeviceSession:
        """Create or update device session for logged-in user."""
        session_key = f"{user.id}:{ip_address}:{user_agent[:100]}"
        session, created = DeviceSession.objects.update_or_create(
            session_key=session_key,
            defaults={
                "user": user,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "is_active": True,
                "last_activity_at": timezone.now(),
            }
        )
        return session

    @staticmethod
    def get_active_sessions(user: User):
        return DeviceSession.objects.filter(user=user, is_active=True)

    @staticmethod
    def revoke_session(user: User, session_id: str):
        DeviceSession.objects.filter(user=user, id=session_id).update(is_active=False)

    @staticmethod
    def revoke_all_sessions(user: User, exclude_session_id: str = None):
        qs = DeviceSession.objects.filter(user=user, is_active=True)
        if exclude_session_id:
            qs = qs.exclude(id=exclude_session_id)
        qs.update(is_active=False)
