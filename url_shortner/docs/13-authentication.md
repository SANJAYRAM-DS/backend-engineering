# 13 — User Authentication (JWT & Password Security)

## 1. Learning Objective
Implement stateless JSON Web Token (JWT) authentication, password hashing with Bcrypt, and token validation middleware in FastAPI.

---

## 2. JWT Tokens Architecture

```text
[ Client ] ──> POST /api/v1/auth/login (email, password)
                   │
                   ▼
       [ Verify Bcrypt Password ]
                   │
                   ▼
     [ Generate Signed JWT Token ] ──> Returns { access_token: "eyJhbG..." }
```

---

## 3. JWT Header & Payload Structure

- **Header**: Algorithm used (`HS256`).
- **Payload**: User claims (`sub: user_id`, `exp: timestamp`, `email`).
- **Signature**: `HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), SECRET_KEY)`.

---

## 4. Implementation Code

```python
import jwt
import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str, expires_delta: datetime.timedelta = datetime.timedelta(hours=24)) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```
