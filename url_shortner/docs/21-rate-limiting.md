# 21 — Distributed Rate Limiting (Sliding Window Algorithm)

## 1. Learning Objective
Implement API rate limiting to protect the URL shortener from DDoS attacks, brute-force short code enumeration, and scraping using Redis sliding window logs.

---

## 2. Algorithms Compared

- **Fixed Window**: Counters reset every minute. Vulnerable to traffic bursts at window boundaries (e.g., 100 requests at 00:59 + 100 requests at 01:01).
- **Token Bucket**: Refills tokens at constant rate. Excellent for bursting.
- **Sliding Window Log (Redis Sorted Set)**: Tracks exact request timestamps per IP/user. Most accurate distributed rate limiting algorithm.

---

## 3. Sliding Window Implementation Code

```python
import time
from fastapi import HTTPException, Request, status
from src.cache.redis_client import redis_client

async def check_rate_limit(request: Request, max_requests: int = 100, window_seconds: int = 60):
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_ip}"
    now = time.time()
    clear_before = now - window_seconds

    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.zremrangebyscore(key, 0, clear_before)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window_seconds)
        results = await pipe.execute()

    request_count = results[2]
    if request_count > max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
```
