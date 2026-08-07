# Phase 20: Custom Security Middleware

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 20 of 35  
> **Target Path**: `docs/20-middleware.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Building custom Django middleware to inject security headers into every HTTP response.
* Creating authentication context providers for Django Ninja API requests.
* Intercepting request/response lifecycles to calculate request execution timing.

---

## 2. Code Implementation & Steps

### Step 1: Security Headers Middleware (`core/middleware.py`)

File path: `core/middleware.py`

```python
"""
Custom Security Headers Middleware.
Applies OWASP recommended security headers to all outgoing responses.
"""
import time
from typing import Callable
from django.http import HttpRequest, HttpResponse

class SecurityHeadersMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Calculate execution latency
        duration_ms = round((time.time() - start_time) * 1000, 2)
        response["X-Response-Time-MS"] = str(duration_ms)

        # OWASP Security Headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
        
        return response
```

---

## 3. Mentor Mode: Self-Check

### Self-Check Questions
1. What threat does the `X-Content-Type-Options: nosniff` header defend against?  
   *Answer: MIME-sniffing attacks. It prevents browsers from trying to guess/override the MIME type of a file served by the server (e.g., executing an uploaded image file as JavaScript).*
