# Phase 05: Enterprise Project Setup & Clean Architecture

> **Phase**: 05 of 35  
> **Target Path**: `docs/05-project-setup.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Structuring Django as a **Modular Monolith** separating identity, authentication, authorization, and audit logs.
* Configuring multi-environment Django settings (`base.py`, `development.py`, `production.py`).
* Wiring **Django Ninja API (`NinjaAPI`)** with custom global exception handlers.

---

## 2. Architecture & File Layout

```text
config/
├── settings/
│   ├── base.py         # Shared core settings
│   ├── development.py  # Local dev overrides
│   └── production.py   # Production lockdown settings
├── api.py              # Central NinjaAPI instance & routers
└── urls.py             # Root URL routing table
```

---

## 3. Code Implementation & Steps

### Step 1: Base Settings (`config/settings/base.py`)

File path: `config/settings/base.py`

```python
"""
Django Base Settings for Enterprise Auth System.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party Apps
    "corsheaders",
    # Local Application Modules
    "apps.users",
    "apps.authentication",
    "apps.audit",
    "apps.rbac",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "config.urls"

# Custom User Model definition
AUTH_USER_MODEL = "users.User"

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "auth_system_db"),
        "USER": os.getenv("POSTGRES_USER", "auth_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "secure_password"),
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### Step 2: Django Ninja API Instance (`config/api.py`)

File path: `config/api.py`

```python
"""
Central Django Ninja API router instance configuration.
"""
from ninja import NinjaAPI
from core.exceptions import BaseAppException
from django.http import JsonResponse

api = NinjaAPI(
    title="Authentication API",
    version="1.0.0",
    description="Authentication & Authorization API",
    docs_url="/docs",
)

@api.exception_handler(BaseAppException)
def app_exception_handler(request, exc: BaseAppException):
    """Global custom exception handler for clean JSON responses."""
    return JsonResponse(
        {
            "status": "error",
            "message": exc.message,
            "details": exc.details,
        },
        status=exc.status_code,
    )
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. Why do we set `AUTH_USER_MODEL = "users.User"` in `base.py` before running initial migrations?  
   *Answer: Changing the User model mid-project in Django requires complex migration refactoring. Setting it upfront prevents database migration breakage.*