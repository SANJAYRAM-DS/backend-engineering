# 14 — Authorization & IDOR Vulnerability Mitigation

## 1. Learning Objective
Learn to prevent Insecure Direct Object Reference (IDOR) vulnerabilities by enforcing resource ownership checks on management endpoints (`DELETE /api/v1/urls/{short_code}`).

---

## 2. What is an IDOR Vulnerability?
An IDOR attack occurs when an API endpoint accepts an identifier (e.g., `DELETE /api/v1/urls/aB72x`) without verifying whether the currently authenticated user owns that specific resource. User A could issue HTTP DELETE requests for User B's short links!

---

## 3. Secure Ownership Enforcement

```python
async def delete_user_url(db: AsyncSession, short_code: str, current_user_id: str):
    url_record = await repo.get_by_short_code(short_code)
    if not url_record:
        raise HTTPException(status_code=404, detail="Link not found")
    if url_record.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this link")
    
    url_record.is_active = False
    await db.commit()
```
