# 19 — Cache Invalidation & Expiration Policies

## 1. Learning Objective
Solve Phil Karlton's classic computer science problem: *"There are only two hard things in Computer Science: cache invalidation and naming things."*

---

## 2. Invalidation Approaches

1. **Time-To-Live (TTL) Eviction**: Automatically drop cached items after $N$ seconds.
2. **Explicit Active Invalidation**: When a user updates or soft-deletes a URL target, delete the key from Redis (`DEL url:aB72x`).
3. **Cache Penetration Protection (Null Caching)**: If a short code does not exist in DB, cache a dummy `NULL` marker in Redis for 60 seconds to prevent attackers from spamming invalid short codes directly to PostgreSQL.

---

## 3. Implementation Code

```python
async def delete_url_and_invalidate_cache(short_code: str):
    # 1. Update Database
    await repo.deactivate_url(short_code)
    # 2. Invalidate Redis Cache Key
    await redis_client.delete(f"url:{short_code}")
```
