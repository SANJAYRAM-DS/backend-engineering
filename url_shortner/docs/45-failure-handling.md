# 45 — Comprehensive Failure Engineering & Graceful Degradation

## 1. Learning Objective
Design graceful degradation strategies when Redis, PostgreSQL, or Kafka infrastructure components experience total failure.

---

## 2. Infrastructure Failure Matrix

| Failed Component | Impact | Graceful Degradation Strategy |
| :--- | :--- | :--- |
| **Redis Down** | Cache misses for all reads | Fallback to PostgreSQL queries with circuit breaker rate-limiting. |
| **PostgreSQL Primary Down** | URL creation fails | Serve existing active short link redirections directly from Redis cache! |
| **Kafka Down** | Analytics events cannot publish | Buffer analytics events in local Redis queue; replay to Kafka upon recovery. |
| **PostgreSQL Replica Down** | Read queries hit primary | Route 100% of read traffic to active replicas and Redis. |
