# Concept 08 — In-Memory Caching & Redis Patterns

# 1. Why PostgreSQL Needs Caching
Under heavy read volume (e.g., 50,000 requests/sec), PostgreSQL disk B-Tree index lookups saturate CPU and disk I/O.

Redis stores key-value pairs entirely in RAM, returning lookups in **< 0.5 ms** (versus 5ms-15ms for database NVMe disk hits).

---

# 2. Cache-Aside (Lazy Loading) Execution Flow

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

# 3. Cache Terminology
- **Cache Hit**: Key found in Redis. Responds immediately.
- **Cache Miss**: Key missing from Redis. Queries PostgreSQL and populates cache.
- **TTL (Time-To-Live)**: Automatic expiration setting (e.g., key evicted after 3,600 seconds).
- **Eviction Policies**: `volatile-lru` drops least-recently-used keys when RAM fills up.
