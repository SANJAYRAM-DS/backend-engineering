# Phase 13: JWT Architecture & Anatomy

> **Phase**: 13 of 35  
> **Target Path**: `docs/13-jwt-architecture.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* The cryptographic structure of JSON Web Tokens (JWT): Header, Payload, Signature.
* Registering and enforcing standard claims (`iss`, `sub`, `aud`, `exp`, `iat`, `jti`).
* Issuing and decoding stateless Access Tokens with `PyJWT`.

---

## 2. JWT Structural Anatomy

```text
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 (Header: Algorithm & Token Type)
. eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ (Payload: Claims)
. SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c (Signature: Cryptographic HMAC-SHA256)
```

---

## 3. Code Implementation & Steps

### Step 1: JWT Service Module (`apps/authentication/jwt.py`)

File path: `apps/authentication/jwt.py`

```python
"""
PyJWT Token Generation & Decoding Service.
Generates cryptographically signed access tokens with custom & standard claims.
"""
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from django.conf import settings
from core.exceptions import AuthenticationError

class JWTService:
    SECRET_KEY = getattr(settings, "JWT_SECRET_KEY", settings.SECRET_KEY)
    ALGORITHM = getattr(settings, "JWT_ALGORITHM", "HS256")
    ACCESS_TTL_MINUTES = getattr(settings, "JWT_ACCESS_TOKEN_LIFETIME_MINUTES", 15)

    @classmethod
    def create_access_token(cls, user_id: str, email: str) -> str:
        """
        Creates short-lived access token with user claims and JTI identifier.
        """
        now = datetime.now(timezone.utc)
        payload = {
            "iss": "auth-system",
            "sub": str(user_id),
            "email": email,
            "token_type": "access",
            "jti": str(uuid.uuid4()),
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=cls.ACCESS_TTL_MINUTES),
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        """
        Decodes and verifies JWT signature and expiration.
        """
        try:
            payload = jwt.decode(
                token,
                cls.SECRET_KEY,
                algorithms=[cls.ALGORITHM],
                options={"verify_signature": True, "verify_exp": True},
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Access token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid access token.")
```

---

## 4. Mentor Mode: Self-Check

### Self-Check Questions
1. What is the role of the `jti` (JWT ID) claim in access tokens?  
   *Answer: `jti` provides a unique identifier for every token issued. It enables specific token blacklisting and prevents replay attacks.*
