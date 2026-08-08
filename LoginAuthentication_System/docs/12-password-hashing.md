# Phase 12: Password Hashing Cryptography (bcrypt / Argon2id)

> **Phase**: 12 of 35  
> **Target Path**: `docs/12-password-hashing.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* The mathematics and cryptography of Key Derivation Functions (KDFs) vs standard hash functions (SHA-256 vs bcrypt/Argon2id).
* Configuring salt generation and tuning work factors (cost factor / memory limits) against GPU-accelerated cracking.
* Preventing timing side-channel attacks using constant-time string comparisons (`hmac.compare_digest`).
* Implementing password re-hashing strategy when work factors or algorithm standards upgrade.

---

## 2. Cryptographic Hashing Theory & Comparison

| Hashing Algorithm | Category | Salt Included? | GPU/ASIC Resistant? | Primary Defense | Recommended Settings |
|---|---|---|---|---|---|
| **MD5 / SHA-1** | Obsolete Hash | No (Manual) | ❌ Extremely Vulnerable | None (Broken) | ⛔ NEVER USE |
| **SHA-256 / SHA-512** | Fast Hash | No (Manual) | ❌ Vulnerable (Billions/sec) | Integrity Check Only | ⛔ DO NOT USE FOR PASSWORDS |
| **PBKDF2-HMAC-SHA256** | Key Derivation | Yes | ⚠️ Moderate | Iterative Hashing | 600,000+ Iterations |
| **bcrypt** | Key Derivation | Yes (24-byte) | ✅ High | Work Cost (Exponential) | Cost Factor 12+ |
| **Argon2id** | Password Hashing (PHC Winner) | Yes (16-byte+) | ✅ Maximum (Memory-Hard) | Time + Memory Hardness | m=64MB, t=3, p=4 |

### Why Fast Hashes (SHA-256) Fail for Passwords
Fast cryptographic hash functions like SHA-256 are engineered for **speed** (verifying file integrity in milliseconds). An modern attacker with an NVIDIA RTX 4090 GPU can compute over **15 billion SHA-256 hashes per second**, rendering saltless or fast-hashed passwords trivial to crack via brute-force or dictionary lookup.

Password Key Derivation Functions (Argon2id / bcrypt) are deliberately **slow and resource-intensive**, forcing GPUs to exhaust memory and computation, reducing cracking speed from billions to a few hundred per second.

---

## 3. Production Password Hashing Service Implementation

File path: `core/security/crypto.py`

```python
"""
Cryptographic Password Hashing Utility supporting Argon2id and bcrypt.
Includes constant-time comparison and dynamic work-factor verification.
"""
import hmac
from passlib.context import CryptContext
from core.exceptions import SecurityException

# Configure Passlib context with Argon2id primary and bcrypt fallback
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,        # 3 iterations
    argon2__parallelism=4,      # 4 parallel threads
    bcrypt__rounds=12,          # Cost factor 2^12
)


class PasswordHasher:
    
    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hashes a plain-text password using the primary configured algorithm (Argon2id).
        Includes automatic cryptographic salt generation.
        """
        if not plain_password:
            raise SecurityException("Cannot hash empty password string.", status_code=400)
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain-text password against a stored hash in constant time.
        """
        if not plain_password or not hashed_password:
            return False
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """
        Checks if the stored password hash used an outdated scheme or lower work factor.
        Used during login to silently upgrade hashes without disrupting user experience.
        """
        return pwd_context.needs_update(hashed_password)

    @staticmethod
    def secure_compare(val1: str, val2: str) -> bool:
        """
        Constant-time string comparison to prevent timing side-channel attacks.
        """
        return hmac.compare_digest(val1.encode("utf-8"), val2.encode("utf-8"))
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. **What is a "Timing Side-Channel Attack" during password verification, and how does `hmac.compare_digest` prevent it?**  
   *Answer: Standard string comparison (`==`) aborts on the first mismatched character. An attacker measuring sub-millisecond response timing can deduce character by character. `hmac.compare_digest` always checks all characters, taking equal time regardless of where mismatches occur.*

2. **How does the `needs_rehash` pattern work when increasing system security requirements?**  
   *Answer: When work factors are increased (e.g. bcrypt rounds from 10 to 12), existing user hashes remain valid. Upon their next successful login, the system detects `needs_rehash() == True`, re-hashes their plain-text password with the new work factor, and updates the database seamlessly.*

### Practical Exercise
* Implement a background migration utility that identifies legacy hashes (e.g., PBKDF2) and flags user accounts for mandatory hash upgrade upon next login.
