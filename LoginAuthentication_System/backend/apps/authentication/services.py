from datetime import timedelta
from django.utils import timezone
from apps.users.models import User
from apps.authentication.models import BlacklistedToken, RefreshToken
from apps.authentication.rotation import TokenRotationEngine
from apps.authentication.sessions import SessionService
from apps.audit.services import AuditService
from core.security.crypto import hash_token
from core.exceptions import AuthenticationError, AccountLockedError

class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str, ip_address: str, user_agent: str) -> tuple[User, str, str]:
        """Authenticate user credentials with brute force lockout tracking."""
        email = email.lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            AuditService.log_event(
                user=None,
                event_type="user.login.failed",
                ip_address=ip_address,
                user_agent=user_agent,
                status="FAILURE",
                details={"email": email, "reason": "User not found"}
            )
            raise AuthenticationError("Invalid email or password.")

        # Lockout check
        if user.is_locked:
            AuditService.log_event(
                user=user,
                event_type="user.login.blocked",
                ip_address=ip_address,
                user_agent=user_agent,
                status="BLOCKED",
                details={"reason": "Account locked"}
            )
            raise AccountLockedError(f"Account locked until {user.locked_until}. Please try again later.")

        # Password check
        if not user.check_password(password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked_until = timezone.now() + timedelta(minutes=15)
                AuditService.log_event(
                    user=user,
                    event_type="account.locked",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status="BLOCKED",
                    details={"failed_attempts": user.failed_login_attempts}
                )
            user.save(update_fields=["failed_login_attempts", "locked_until"])

            AuditService.log_event(
                user=user,
                event_type="user.login.failed",
                ip_address=ip_address,
                user_agent=user_agent,
                status="FAILURE",
                details={"failed_attempts": user.failed_login_attempts}
            )
            raise AuthenticationError("Invalid email or password.")

        # Success - Reset lockout counter
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = timezone.now()
        user.save(update_fields=["failed_login_attempts", "locked_until", "last_login_at"])

        # Track session
        SessionService.track_session(user, ip_address, user_agent)

        # Issue tokens
        access_token, refresh_token, _ = TokenRotationEngine.issue_token_pair(user)

        AuditService.log_event(
            user=user,
            event_type="user.login.success",
            ip_address=ip_address,
            user_agent=user_agent,
            status="SUCCESS",
            details={}
        )

        return user, access_token, refresh_token

    @staticmethod
    def logout(user: User, jti: str, refresh_token: str = None):
        """Blacklists access token and revokes refresh token."""
        if jti:
            BlacklistedToken.objects.get_or_create(
                jti=jti,
                defaults={
                    "user": user,
                    "token_type": "access",
                    "expires_at": timezone.now() + timedelta(minutes=15),
                    "reason": "user_logout"
                }
            )
        if refresh_token:
            token_digest = hash_token(refresh_token)
            RefreshToken.objects.filter(token_hash=token_digest).update(is_revoked=True)
