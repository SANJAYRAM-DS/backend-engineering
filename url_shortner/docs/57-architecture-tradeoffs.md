# 57 — Master Architectural Trade-Off Analysis Matrix

## 1. Learning Objective
Synthesize key engineering trade-offs made across database design, ID generation, caching, messaging, and scaling.

---

## 2. Trade-Off Analysis Table

| Decision Area | Option A | Option B | Selected Option | Justification |
| :--- | :--- | :--- | :--- | :--- |
| **Redirect Status Code** | 301 Permanent | 302 Found | **302 Found** | 301 breaks click analytics due to aggressive browser caching. |
| **ID Encoding** | Base64 | Base62 | **Base62** | Base64 contains reserved characters (`+`, `/`) unsafe in URLs without escaping. |
| **Caching Pattern** | Write-Through | Cache-Aside | **Cache-Aside** | Only active hot links consume Redis RAM; avoids caching cold, single-use links. |
| **Click Telemetry Ingestion** | Synchronous DB Insert | Async Kafka Pipeline | **Async Kafka** | Removes disk write I/O latency from the user HTTP redirection path. |
| **ID Generation** | Central Auto-Increment | Twitter Snowflake | **Twitter Snowflake** | Prevents database lock contention across multiple API nodes. |
