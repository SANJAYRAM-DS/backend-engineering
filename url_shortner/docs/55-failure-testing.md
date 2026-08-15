# 55 — Chaos Engineering & Failure Injection Testing

## 1. Learning Objective
Perform intentional Chaos Engineering experiments by killing Redis, PostgreSQL, and Kafka containers during high load to verify system resiliency.

---

## 2. Chaos Injection Commands

```bash
# 1. Start Load Test
locust -f tests/load/locustfile.py &

# 2. Chaos Injection: Kill Redis Container
docker stop url_shortener_redis

# 3. Observe API Behavior
# Expected Result: API logs warning, falls back to PostgreSQL, redirection continues at higher DB latency!

# 4. Recover Redis Container
docker start url_shortener_redis
# Expected Result: Circuit breaker closes, cache misses populate Redis, latency returns to < 2ms!
```
