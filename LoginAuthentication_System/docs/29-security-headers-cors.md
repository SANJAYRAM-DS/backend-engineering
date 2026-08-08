# Phase 29: Enterprise Security Headers & CORS Lockdown

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 29 of 35  
> **Target Path**: `docs/29-security-headers-cors.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Configuring **Cross-Origin Resource Sharing (CORS)** allowlists to block untrusted domains.
* Implementing uniform JSON exception handlers that hide sensitive stack traces from production responses.

---

## 2. Code Implementation & Steps

### Step 1: CORS Settings Blueprint (`config/settings/production.py`)

File path: `config/settings/production.py`

```python
"""
Production Hardening & Security Configuration.
"""
import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "api.authsystem.com").split(",")

# Strict CORS configuration
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "https://app.authsystem.com").split(",")
CORS_ALLOW_CREDENTIALS = True

# HTTPS Lockdown
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 3. Mentor Mode: Self-Check

### Self-Check Questions
1. Why is setting `CORS_ALLOW_ALL_ORIGINS = True` dangerous when using `CORS_ALLOW_CREDENTIALS = True`?  
   *Answer: Modern browsers automatically reject requests that specify both wildcards (`*`) and credentials (`withCredentials: true`). Allowing all origins with credentials opens the API to cross-origin data theft.*
