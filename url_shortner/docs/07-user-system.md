# 07 — User System & User Management

## 1. Learning Objective
Learn how to design and build a multi-tenant user account system to support authenticated link creation, ownership, and user dashboard management.

---

## 2. Problem
Without user accounts, all shortened links are anonymous and unowned. Users cannot manage, edit, delete, or view private analytics for their created links.

---

## 3. Theory & Concepts
User data management requires:
- Password hashing with **Bcrypt** / **Argon2** (never store plaintext passwords!).
- Unique email constraints.
- Foreign key relationship (`urls.user_id -> users.id`).

---

## 4. Architecture

```text
[ Client ] ──> POST /api/v1/auth/register ──> [ Auth Service ] ──> [ Users Table ]
                                                                          │
[ Client ] ──> POST /api/v1/urls (with Auth Token) ───────────────────────┼──> [ Link Created with user_id ]
```

---

## 5. SQL Schema Extensions

```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE urls ADD CONSTRAINT fk_urls_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;
```

---

## 6. Complete Python Implementation Code

### Model Definition (`src/db/models.py`)
```python
import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

---

## 7. Verification & Exercises
1. **Exercise**: Add a unique index on `LOWER(email)` to prevent case-sensitivity duplicate account registration (`User@Example.com` vs `user@example.com`).
2. **Interview Question**: Why is SHA-256 unsuitable for password hashing, and why do password hashing algorithms like Bcrypt/Argon2 intentionally include salt and work factors?
