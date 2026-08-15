# 17 — In-Memory Caching & Redis Fundamentals

## 1. Learning Objective
Understand why relational databases become bottlenecks under high read throughput and learn how Redis achieves sub-millisecond lookups via in-memory data structures.

---

## 2. Why PostgreSQL Needs Caching

| Operational Metric | PostgreSQL (NVMe Disk/B-Tree) | Redis (In-Memory Key-Value) |
| :--- | :--- | :--- |
| **Lookup Latency** | 2ms - 15ms | **0.2ms - 0.8ms** |
| **Max Read QPS (Single Node)** | ~3,000 QPS | **~100,000 QPS** |
| **Storage Medium** | Disk (NVMe/SSD) | RAM |

---

## 3. Redis Data Structures & Key Design

- **Strings**: `SET url:aB72x "https://example.com/long-target"` (Simple key-value lookup).
- **Hashes**: `HSET url_meta:aB72x target "https://..." clicks 45 created "2026-08-15"`.
- **HyperLogLogs**: `PFADD unique_visitors:aB72x "192.168.1.1"` (Memory-efficient distinct IP counter using ~12 KB RAM).

---

## 4. Redis Client Setup Code (`src/cache/redis_client.py`)

```python
import redis.asyncio as aioredis
from src.core.config import settings

redis_client = aioredis.from_url(
    settings.assemble_redis_url(),
    encoding="utf-8",
    decode_responses=True,
)

async def get_cache(key: str) -> str | None:
    return await redis_client.get(key)

async def set_cache(key: str, value: str, ttl_seconds: int = 3600):
    await redis_client.set(key, value, ex=ttl_seconds)
```
