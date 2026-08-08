import uuid
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )
    event_type = models.CharField(max_length=100, db_index=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    status = models.CharField(max_length=20, choices=[("SUCCESS", "Success"), ("FAILURE", "Failure"), ("BLOCKED", "Blocked")])
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-created_at"]
