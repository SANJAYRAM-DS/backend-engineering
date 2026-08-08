# Phase 19: HTTP-Only Dual Cookie & Bearer Transport Engine

> **Phase**: 19 of 35  
> **Target Path**: `docs/19-http-only-cookie-bearer.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Dual-mode authentication transport supporting both web frontend clients (cookies) and mobile/external API consumers (`Bearer` headers).
* Configuring secure cookie flags (`HttpOnly`, `SameSite=Lax/Strict`, `Secure`, `Domain`, `Path`) to eliminate XSS token theft.
* Protecting cookie-authenticated endpoints against Cross-Site Request Forgery (CSRF) via Double-Submit Cookie patterns and custom headers.
* Injecting response cookies dynamically in Django / Django Ninja view functions.

---

## 2. Cookie Security Attributes & Matrix

| Flag / Attribute | Value | Security Protection |
|---|---|---|
| **HttpOnly** | `True` | Prevents Client-side JavaScript (`document.cookie`) from reading tokens, completely mitigating **XSS token theft**. |
| **Secure** | `True` | Restricts cookie transmission exclusively over encrypted **HTTPS** connections. |
| **SameSite** | `Lax` / `Strict` | Restricts cross-origin requests, blocking automated **CSRF attacks**. |
| **Path** | `/api/v1/auth/refresh` | Scopes refresh token cookies exclusively to auth endpoints, preventing leak to public routes. |

---

## 3. Dual Transport Extraction & Response Injection

File path: `core/security/transport.py`

```python
"""
Dual Token Transport Layer: Supports Authorization Header and HttpOnly Cookie extraction.
"""
from typing import Optional
from ninja.security import HttpBearer
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from core.security.tokens import AccessTokenEngine
from core.exceptions import AuthenticationException


class DualTokenAuth(HttpBearer):
    """
    Django Ninja Security Guard: 
    1. Checks 'Authorization: Bearer <token>' header first.
    2. Falls back to 'access_token' HttpOnly cookie if header is absent.
    """
    def authenticate(self, request: HttpRequest, token: str) -> Optional[dict]:
        # 1. Try header token
        if token:
            return AccessTokenEngine.decode_and_verify_access_token(token)
        
        # 2. Try cookie token if header missing
        cookie_token = request.COOKIES.get("access_token")
        if cookie_token:
            return AccessTokenEngine.decode_and_verify_access_token(cookie_token)

        raise AuthenticationException("Missing authentication credentials.", status_code=401)


class CookieManager:

    @staticmethod
    def set_auth_cookies(
        response: HttpResponse, 
        access_token: str, 
        refresh_token: str
    ) -> HttpResponse:
        """
        Attaches HttpOnly, Secure, SameSite cookies to the outgoing HTTP response object.
        """
        # Access Token Cookie (Short lived: 15 min)
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            path="/"
        )

        # Refresh Token Cookie (Longer lived: 7 days, scoped path)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 86400,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            path="/api/v1/auth/"
        )

        return response

    @staticmethod
    def clear_auth_cookies(response: HttpResponse) -> HttpResponse:
        """
        Deletes authentication cookies during logout.
        """
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/api/v1/auth/")
        return response
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. **Why is storing JWT access tokens in `localStorage` or `sessionStorage` insecure for web applications?**  
   *Answer: Any Third-Party JavaScript dependency or XSS vulnerability on the site can read `localStorage` and exfiltrate raw tokens to an attacker server. `HttpOnly` cookies block JS read access entirely.*

2. **Why do we scope the `refresh_token` cookie `Path` exclusively to `/api/v1/auth/`?**  
   *Answer: Scoping limits cookie exposure. The refresh token cookie is only transmitted by the browser when hitting authentication endpoints (like token rotation or logout), keeping standard API calls lightweight and secure.*

### Practical Exercise
* Configure CORS (`django-cors-headers`) settings with `CORS_ALLOW_CREDENTIALS = True` and specific trusted `CORS_ALLOWED_ORIGINS`, verifying that wildcard origins (`*`) are disallowed when using cookies.
