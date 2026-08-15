# Concept 16 — Authentication, Authorization & Security Controls

# 1. Authentication (JWT)
Stateless authentication using signed JSON Web Tokens (JWT):

```text
Header.Payload.Signature
```

- **Password Hashing**: Bcrypt / Argon2 with salt and cost factor (never store plaintext!).
- **Stateless Tokens**: API nodes verify JWT signatures using `SECRET_KEY` without querying database.

---

# 2. Authorization & IDOR Defense
Insecure Direct Object Reference (IDOR) occurs when an endpoint accepts `DELETE /api/v1/urls/{short_code}` without validating resource ownership.

Enforce strict checks:
`IF url.user_id != current_user.id THEN RETURN 403 Forbidden`
