import uuid
from datetime import datetime, timedelta, timezone
from django.db import transaction
from apps.users.models import User
from apps.authentication.models import RefreshToken
from apps.audit.services import AuditService
from core.config import settings
from core.security.crypto import hash_token, generate_opaque_token
from core.security.tokens import create_access_token
from core.exceptions import AuthenticationError, TokenReuseError

class TokenRotationEngine:
    @staticmethod
    @transaction.atomic
    def issue_token_pair(user: User, family_id: uuid.UUID = None) -> tuple[str, str, str]:
        """Issues short-lived access token and long-lived refresh token."""
        roles = list(user.user_roles.values_list("role__name", flat=True))
        access_token, jti = create_access_token(user_id=str(user.id), email=user.email, roles=roles)
        
        raw_refresh_token = generate_opaque_token(48)
        hashed_refresh = hash_token(raw_refresh_token)
        
        if not family_id:
            family_id = uuid.uuid4()
            
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        RefreshToken.objects.create(
            user=user,
            token_hash=hashed_refresh,
            family_id=family_id,
            expires_at=expires_at
        )
        
        return access_token, raw_refresh_token, jti

    @staticmethod
    @transaction.atomic
    def rotate_refresh_token(raw_refresh_token: str, ip_address: str, user_agent: str) -> tuple[str, str]:
        """Performs Refresh Token Rotation with automatic reuse detection."""
        token_digest = hash_token(raw_refresh_token)
        try:
            token_record = RefreshToken.objects.select_related("user").get(token_hash=token_digest)
        except RefreshToken.DoesNotExist:
            raise AuthenticationError("Invalid refresh token.")

        # Expiration Check
        if token_record.expires_at < datetime.now(timezone.utc):
            raise AuthenticationError("Refresh token has expired.")

        # Revocation Check
        if token_record.is_revoked:
            raise AuthenticationError("Refresh token has been revoked.")

        # REUSE DETECTION ENGINE
        if token_record.is_consumed:
            # Token reuse breach detected! Revoke whole family lineage immediately.
            RefreshToken.objects.filter(family_id=token_record.family_id).update(is_revoked=True)
            
            AuditService.log_event(
                user=token_record.user,
                event_type="token.reuse_hijack_detected",
                ip_address=ip_address,
                user_agent=user_agent,
                status="BLOCKED",
                details={"family_id": str(token_record.family_id), "token_id": str(token_record.id)}
            )
            
            raise TokenReuseError("Security Alert: Reused refresh token detected. Entire session family revoked.")

        # Normal Rotation Path: Mark consumed and issue new child token in same family
        token_record.is_consumed = True
        token_record.save(update_fields=["is_consumed"])

        new_access, new_refresh, _ = TokenRotationEngine.issue_token_pair(
            user=token_record.user,
            family_id=token_record.family_id
        )

        AuditService.log_event(
            user=token_record.user,
            event_type="token.rotated",
            ip_address=ip_address,
            user_agent=user_agent,
            status="SUCCESS",
            details={"family_id": str(token_record.family_id)}
        )

        return new_access, new_refresh
