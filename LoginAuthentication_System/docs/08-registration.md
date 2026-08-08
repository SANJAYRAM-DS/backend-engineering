# Phase 08: User Registration Workflow & Validation

> **Phase**: 08 of 35  
> **Target Path**: `docs/08-registration.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Implementing atomic registration pipelines using Django's `@transaction.atomic`.
* Building Pydantic V2 input schemas enforcing strict password entropy and sanitization.
* Returning sanitized response DTOs that exclude sensitive fields like password hashes.

---

## 2. Pydantic Validation & Security Schemas

File path: `apps/users/schemas.py`

```python
"""
Pydantic V2 Schemas for User Registration and Profile Response.
"""
import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=12, max_length=128)
    first_name: Optional[str] = Field(default="", max_length=100)
    last_name: Optional[str] = Field(default="", max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """Enforces complexity: uppercase, lowercase, digit, and special char."""
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numeric digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

---

## 3. Registration Service Layer

File path: `apps/users/services.py`

```python
"""
User Service Domain Layer.
Encapsulates business logic for user account creation.
"""
from django.db import transaction
from apps.users.models import User
from apps.users.schemas import UserRegisterSchema
from core.exceptions import BaseAppException

class UserService:
    
    @staticmethod
    @transaction.atomic
    def register_user(payload: UserRegisterSchema) -> User:
        """
        Atomically creates a new user account if the email is not already registered.
        """
        email_clean = payload.email.lower().strip()
        if User.objects.filter(email=email_clean).exists():
            raise BaseAppException(
                message="An account with this email address already exists.",
                status_code=409,
            )
        
        user = User.objects.create_user(
            email=email_clean,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        return user
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. Why is `@transaction.atomic` critical during user registration when email verification tokens or initial profile records are generated?  
   *Answer: It ensures atomic execution. If token creation or email sending fails, the database automatically rolls back user record creation, preventing orphaned state.*
