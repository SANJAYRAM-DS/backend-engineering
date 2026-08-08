import uuid
from django.db import models
from django.conf import settings

class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="refresh_tokens")
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    family_id = models.UUIDField(db_index=True)
    
    is_revoked = models.BooleanField(default=False)
    is_consumed = models.BooleanField(default=False)
    
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_refreshtoken"


class BlacklistedToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blacklisted_tokens")
    jti = models.CharField(max_length=255, unique=True, db_index=True)
    token_type = models.CharField(max_length=20, choices=[("access", "Access"), ("refresh", "Refresh")])
    expires_at = models.DateTimeField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, default="logout")

    class Meta:
        db_table = "auth_blacklistedtoken"


class DeviceSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_sessions")
    session_key = models.CharField(max_length=255, unique=True, db_index=True)
    ip_address = models.CharField(max_length=45, default="127.0.0.1")
    user_agent = models.TextField(default="Unknown")
    device_type = models.CharField(max_length=50, default="Web Client")
    is_active = models.BooleanField(default=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_device_session"
        ordering = ["-last_activity_at"]
