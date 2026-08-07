# Phase 10: Email Verification Engine

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 10 of 35  
> **Target Path**: `docs/10-email-verification.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Generating stateless cryptographic verification tokens using `django.core.signing.TimestampSigner`.
* Building an asynchronous email delivery service structure.
* Validating single-use email verification tokens with expiration checking.

---

## 2. Code Implementation & Steps

### Step 1: Email Verification Token Service (`apps/users/tokens.py`)

File path: `apps/users/tokens.py`

```python
"""
Cryptographic Token Signing Engine for Email Verification and Password Reset.
Uses HMAC-SHA256 timestamp signing to avoid database state overhead for tokens.
"""
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from core.exceptions import BaseAppException

class EmailVerificationTokenService:
    SALT = "apps.users.email_verification"

    @classmethod
    def generate_token(cls, user_id: str) -> str:
        """Generates a cryptographically signed token containing user_id."""
        signer = TimestampSigner(salt=cls.SALT)
        return signer.sign(str(user_id))

    @classmethod
    def verify_token(cls, token: str, max_age_seconds: int = 86400) -> str:
        """
        Verifies token signature and checks timestamp expiry (default 24 hours).
        Returns un-signed user_id string if valid.
        """
        signer = TimestampSigner(salt=cls.SALT)
        try:
            user_id = signer.unsign(token, max_age=max_age_seconds)
            return user_id
        except SignatureExpired:
            raise BaseAppException("Email verification token has expired.", status_code=400)
        except BadSignature:
            raise BaseAppException("Invalid email verification token.", status_code=400)
```

---

## 3. Mentor Mode: Self-Check

### Self-Check Questions
1. What is the advantage of using `TimestampSigner` over storing email verification tokens in PostgreSQL?  
   *Answer: Stateless verification. `TimestampSigner` includes the creation timestamp and HMAC signature in the token string itself, requiring zero database storage or lookup during signature validation.*
