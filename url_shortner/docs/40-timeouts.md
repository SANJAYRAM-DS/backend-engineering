# 40 — Timeouts & Preventing Cascading Failures

## 1. Learning Objective
Implement strict network timeouts across Redis, PostgreSQL, and external HTTP calls to prevent thread exhaustion during downstream latency spikes.

---

## 2. Setting Timeouts in Async Code

```python
# PostgreSQL Connection Timeout
engine = create_async_engine(..., connect_args={"command_timeout": 3})

# Redis Timeout
redis_client = aioredis.from_url(..., socket_timeout=0.5, socket_connect_timeout=0.5)
```
