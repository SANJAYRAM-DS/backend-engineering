# Phase 11 & 12: Secure Login Pipeline & Password Hashing Cryptography

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 11 & 12 of 35  
> **Target Path**: `docs/11-login.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Password hashing internal workings: Salt, Work Factor (Cost), Key Derivation Functions (Argon2id, bcrypt, PBKDF2).
* Implementing constant-time credential checking to prevent User Enumeration and Timing Attacks.
* Updating user login audit fields (`last_login_at`) upon authentication.

---

## 2. Cryptographic Password Hashing Theory

```text
[ Plaintext Password: "P@ssw0rd12345!" ] 
                + 
[ Cryptographic Salt: 16 Random Bytes ]
                |
                v
  [ Cost Factor 12 Key Derivation (2^12 Iterations) ]
                |
                v
[ Stored Hash: $2b$12$eImiTXuWVxfM37uY4JANjO.gQz6F.zV1uX.eGz8k7/1O2P3Q4R5S6 ]
```

---

## 3. Code Implementation & Steps

### Step 1: Authentication Logic (`apps/authentication/services.py`)

File path: `apps/authentication/services.py`

```python
"""
Authentication & Login Service Engine.
Handles credential verification, constant-time hashing checks, and account status checks.
"""
from django.utils import timezone
from apps.users.models import User
from core.exceptions import AuthenticationError

class AuthenticationService:

    @staticmethod
    def authenticate_credentials(email: str, password: str) -> User:
        """
        Authenticates user email and password using constant-time evaluation.
        Prevents user enumeration by executing password hash check even if user doesn't exist.
        """
        email_clean = email.lower().strip()
        try:
            user = User.objects.get(email=email_clean)
        except User.DoesNotExist:
            user = None

        if user is not None:
            password_valid = user.check_password(password)
        else:
            # Dummy hash check to consume constant CPU time and prevent timing attacks
            User().set_password("dummy_password_for_timing")
            password_valid = False

        if user is None or not password_valid:
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("This account has been deactivated.")

        if user.is_locked:
            raise AuthenticationError("Account is temporarily locked due to failed attempts.")

        # Reset failed attempts and update last login
        user.failed_login_attempts = 0
        user.last_login_at = timezone.now()
        user.save(update_fields=["failed_login_attempts", "last_login_at"])

        return user
```

---

## 4. Mentor Mode: Self-Check

### Self-Check Questions
1. Why do we execute `User().set_password("dummy_password_for_timing")` when a user email is not found?  
   *Answer: bcrypt password verification is computationally expensive (~100ms). If we returned immediately when email wasn't found (in <1ms), attackers could measure API latency to discover registered emails. Dummy execution forces uniform ~100ms response time.*
