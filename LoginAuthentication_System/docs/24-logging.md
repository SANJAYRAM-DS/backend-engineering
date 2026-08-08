# Phase 24: Structured JSON Logging Infrastructure

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 24 of 35  
> **Target Path**: `docs/24-logging.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Structuring security logs in JSON format for SIEM integration (ElasticSearch / Datadog).
* Building an immutable database audit log capturing sensitive operations.
* Masking Personally Identifiable Information (PII) and credentials in log streams.

---

## 2. Code Implementation & Steps

### Step 1: Audit Log Model (`apps/audit/models.py`)

File path: `apps/audit/models.py`

```python
"""
Immutable Security Audit Log Database Model.
"""
import uuid
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="audit_logs")
    event_type = models.CharField(max_length=100, db_index=True) # e.g. "auth.login.success", "auth.token.revoked"
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    status = models.CharField(max_length=20) # "SUCCESS", "FAILURE", "BLOCKED"
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-created_at"]
```

### Step 2: Audit Logging Service (`apps/audit/services.py`)

File path: `apps/audit/services.py`

```python
"""
Audit Logging Helper Service.
"""
import logging
from typing import Any, Dict, Optional
from apps.audit.models import AuditLog
from apps.users.models import User

logger = logging.getLogger("security.audit")

class AuditService:

    @staticmethod
    def log_event(
        event_type: str,
        ip_address: str,
        user_agent: str,
        status: str,
        user: Optional[User] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """
        Writes immutable record to PostgreSQL and emits structured log line.
        """
        details_clean = details or {}
        # Mask sensitive keys if present
        for key in ["password", "token", "secret"]:
            if key in details_clean:
                details_clean[key] = "********"

        audit_entry = AuditLog.objects.create(
            user=user,
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            details=details_clean,
        )

        logger.info(
            f"SECURITY_AUDIT: event={event_type} status={status} user_id={user.id if user else 'anonymous'} ip={ip_address}"
        )
        return audit_entry
```

---

## 3. Mentor Mode: Self-Check

### Self-Check Questions
1. Why should loggers mask fields containing `"password"` or `"token"` before writing log lines?  
   *Answer: To comply with SOC2, GDPR, and PCI-DSS standards. Log files are often stored in unencrypted third-party log aggregators; storing raw passwords in logs compromises user security.*
