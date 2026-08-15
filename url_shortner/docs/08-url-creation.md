# 08 — URL Creation Engine & Alias Collisions

## 1. Learning Objective
Master the URL creation lifecycle, custom alias uniqueness checks, database transactions, and collision mitigation strategies.

---

## 2. Collision Handling Strategies

When generating short codes (e.g., `aB72x`), two strategies exist:

1. **Pre-checking Database / Cache**: Query `SELECT short_code FROM urls WHERE short_code = :code`. If collision occurs, retry with a new code.
2. **Database Unique Constraint Exception Handling**: Rely on `UNIQUE(short_code)` in PostgreSQL. Catch `IntegrityError` on `INSERT` and retry.

```text
               [ Generate Code: "aB72x" ]
                           │
                           ▼
              [ Try DB Insert (Unique Index) ]
                           │
             ┌─────────────┴─────────────┐
             │                           │
     [ Insert Success ]         [ IntegrityError Collision ]
             │                           │
             ▼                           ▼
      [ Return 201 ]            [ Regenerate Code & Retry ]
```

---

## 3. Implementation Code

```python
# Code snippet for src/services/url_service.py
async def create_with_retry(self, request: URLCreateRequest, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await self.repo.create_url(...)
        except IntegrityError:
            if attempt == max_retries - 1:
                raise HTTPException(status_code=500, detail="Failed to generate unique short code.")
```

---

## 4. Verification & Exercises
- Test submitting 100 concurrent creation requests for the same custom alias to verify only 1 succeeds with `201 Created` while 99 fail with `409 Conflict`.
