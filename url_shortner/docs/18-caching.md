# 18 — Caching Strategies: Cache-Aside & Write-Through

## 1. Learning Objective
Implement the **Cache-Aside (Lazy Loading)** caching pattern for URL redirection lookups.

---

## 2. Cache-Aside Execution Sequence

```text
               [ GET /aB72x Request ]
                         │
                         ▼
             [ Query Redis Key "url:aB72x" ]
                         │
             ┌───────────┴───────────┐
             │                       │
      [ Cache HIT ]           [ Cache MISS ]
             │                       │
             ▼                       ▼
      [ Return Target ]       [ Query PostgreSQL ]
                                     │
                                     ▼
                              [ Write to Redis ]
                                     │
                                     ▼
                              [ Return Target ]
```

---

## 3. Implementation Code

```python
async def resolve_url_cached(short_code: str) -> str:
    cache_key = f"url:{short_code}"
    # 1. Try Cache Read
    cached_url = await redis_client.get(cache_key)
    if cached_url:
        return cached_url
    
    # 2. Cache Miss: Fallback to PostgreSQL
    db_record = await repo.get_by_short_code(short_code)
    if not db_record:
        raise HTTPException(status_code=404, detail="Not Found")
    
    # 3. Populate Redis Cache with 1-Hour TTL
    await redis_client.set(cache_key, db_record.original_url, ex=3600)
    return db_record.original_url
```
