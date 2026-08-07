# Phase 06: Environment & Config Management

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 06 of 35  
> **Target Path**: `docs/06-environment-config.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Enforcing the **12-Factor App Methodology (Factor III: Config)** by strictly separating configuration from code.
* Preventing accidental secret exposure using strict `.gitignore` and `.env.example` templates.
* Building a type-safe settings validation module in Python.

---

## 2. Theory & Security Best Practices

### The Dangers of Hardcoded Secrets
* **Git History Pollution**: Committing a secret (e.g., `JWT_SECRET_KEY = "supersecret"`) to Git permanently records it in commit history. Even if deleted in a later commit, automated scrapers can extract it.
* **Rotation Complexity**: If keys are hardcoded in source files, rotating compromised credentials requires code changes, pull requests, and redeployments instead of an environment variable update.

---

## 3. Code Implementation & Steps

### Step 1: Type-Safe Environment Loader (`core/config.py`)

File path: `core/config.py`

```python
"""
Type-Safe Environment Configuration Loader.
Validates required environment variables upon application launch.
"""
import os
from typing import NamedTuple

class EnvironmentConfig(NamedTuple):
    env: str
    debug: bool
    secret_key: str
    jwt_secret_key: str
    jwt_access_ttl_minutes: int
    jwt_refresh_ttl_days: int
    postgres_db: str

def load_environment_config() -> EnvironmentConfig:
    """
    Parses and validates environment variables.
    Raises ValueError if required production keys are missing.
    """
    env = os.getenv("DJANGO_ENV", "development")
    secret_key = os.getenv("SECRET_KEY")
    jwt_secret = os.getenv("JWT_SECRET_KEY")

    if env == "production":
        if not secret_key or secret_key.startswith("django-insecure"):
            raise ValueError("CRITICAL SECURITY ERROR: Insecure DJANGO_SECRET_KEY in production!")
        if not jwt_secret or len(jwt_secret) < 32:
            raise ValueError("CRITICAL SECURITY ERROR: JWT_SECRET_KEY must be at least 32 characters in production!")

    return EnvironmentConfig(
        env=env,
        debug=os.getenv("DEBUG", "False") == "True",
        secret_key=secret_key or "dev-fallback-key",
        jwt_secret_key=jwt_secret or "dev-jwt-fallback-key",
        jwt_access_ttl_minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "15")),
        jwt_refresh_ttl_days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "7")),
        postgres_db=os.getenv("POSTGRES_DB", "auth_system_db"),
    )
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. Why should `JWT_SECRET_KEY` be distinct from `DJANGO_SECRET_KEY`?  
   *Answer: Separation of Concerns & Key Isolation. If one key is leaked or compromised, the impact is isolated to that specific subsystem.*
