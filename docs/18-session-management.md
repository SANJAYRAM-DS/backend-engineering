# Phase 18 & 19: Session Management & Dual Cookie Transport

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 18 & 19 of 35  
> **Target Path**: `docs/18-session-management.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Storing JWT refresh tokens inside secure, `HttpOnly`, `SameSite=Lax`, `Secure` cookies.
* Tracking active client device sessions (IP, User-Agent, last activity).
* Mitigating XSS token theft and CSRF attacks simultaneously.

---

## 2. Cookie Security Configuration

```text
Set-Cookie: refresh_token=uuid_string; 
            HttpOnly;                <-- Blocks JavaScript (document.cookie) XSS access
            Secure;                  <-- Transmitted ONLY over HTTPS
            SameSite=Lax;            <-- Protects against cross-site CSRF forms
            Path=/api/v1/auth;       <-- Restricts cookie scope to auth endpoints
```

---

## 3. Code Implementation & Steps

### Step 1: Session Tracking Model (`apps/authentication/sessions.py`)

File path: `apps/authentication/sessions.py`

```python
"""
Active Device & Session Tracking Infrastructure.
"""
import uuid
from django.db import models
from django.conf import settings

class DeviceSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions")
    session_key = models.CharField(max_length=64, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    is_active = models.BooleanField(default=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_device_session"
```

---

## 4. Mentor Mode: Self-Check

### Self-Check Questions
1. Why is setting `HttpOnly` on JWT cookies critical for modern single-page applications (SPAs)?  
   *Answer: If an attacker finds an XSS vulnerability (injecting `<script>` tags), `HttpOnly` prevents their JavaScript from reading `document.cookie`, keeping the refresh token safe from exfiltration.*
