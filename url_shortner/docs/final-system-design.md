# Master Document: Final Production System Design Blueprint

# 01. Learning Objective

By the end of this document, I should understand:
- The end-to-end architecture of our production-grade URL Shortener system.
- Every architectural component, data flow, storage model, and resilience guarantee.
- How to present this architecture in senior executive reviews and technical interviews.

---

# 02. Final Production Architecture Diagram

```text
                                    [ USER CLIENTS ]
                            (Web Browsers / Mobile Apps / CLI)
                                            │
                                            │ HTTP / HTTPS Requests
                                            v
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                              EDGE LAYER (CDN / WAF)                                   │
│   - Cloudflare CDN Edge Redirection Caching (Cache 302s for non-expired URLs)         │
│   - Anti-DDoS Protection & Web Application Firewall (WAF)                             │
└───────────────────────────────────────────┬───────────────────────────────────────────┘
                                            │
                                            │ Clean HTTP Requests
                                            v
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                            LOAD BALANCER LAYER (AWS ALB)                              │
│   - Layer 7 Path Routing & SSL/TLS Termination                                       │
│   - Health Checks & Round-Robin / Least Connections Load Distribution                 │
└───────────────────────────────────────────┬───────────────────────────────────────────┘
                                            │
                                            v
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                       STATELESS API CLUSTER (FastAPI Containers)                      │
│                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────┐   │
│   │                              1. API LAYER                                     │   │
│   │   - Routers: GET /{short_code}, POST /api/v1/urls, GET /analytics            │   │
│   │   - Middleware: Rate Limiter, Idempotency, JWT Auth, CORS, Security Headers  │   │
│   └───────────────────────────────────────┬───────────────────────────────────────┘   │
│                                           │                                           │
│   ┌───────────────────────────────────────▼───────────────────────────────────────┐   │
│   │                            2. SERVICE LAYER                                   │   │
│   │   - Base62 Encoding Engine & Twitter Snowflake ID Generator                   │   │
│   │   - Local Worker In-Memory LRU Cache (Hot-Key Mitigation)                     │   │
│   │   - Circuit Breakers & Retries with Exponential Backoff + Jitter              │   │
│   └───────────────────────────────────────┬───────────────────────────────────────┘   │
│                                           │                                           │
│   ┌───────────────────────────────────────▼───────────────────────────────────────┐   │
│   │                           3. DATA ACCESS LAYER                                │   │
│   │   - Redis Cache-Aside Manager & Async SQLAlchemy ORM Repository               │   │
│   └─────────────────────────┬───────────────────────────┬─────────────────────────┘   │
└─────────────────────────────┼───────────────────────────┼─────────────────────────────┘
                              │                           │
            ┌─────────────────┘                           └─────────────────┐
            │                                                               │
            v                                                               v
┌──────────────────────────────┐                         ┌──────────────────────────────────┐
│   IN-MEMORY CACHE CLUSTER    │                         │    PERSISTENT DATABASE CLUSTER   │
│       (REDIS CLUSTER)        │                         │       (POSTGRESQL SHARDS)        │
│                              │                         │                                  │
│ - Redis 7 Nodes (3 Shards)   │                         │ - Primary Shard 0 (A-M codes)    │
│ - Consistent Hash Ring       │                         │ - Primary Shard 1 (N-Z codes)    │
│ - Sub-millisecond Lookups    │                         │ - Read Replicas per Shard        │
└──────────────────────────────┘                         └─────────────────┬────────────────┘
                                                                           │
                                                                           │ Asynchronous Event Log
                                                                           v
                                                         ┌──────────────────────────────────┐
                                                         │     EVENT STREAMING (KAFKA)      │
                                                         │                                  │
                                                         │ - Topic: click_events (6 Part)   │
                                                         │ - Partitioned by short_code      │
                                                         └─────────────────┬────────────────┘
                                                                           │
                                                                           v
                                                         ┌──────────────────────────────────┐
                                                         │   ANALYTICS & FRAUD WORKERS      │
                                                         │                                  │
                                                         │ - Bulk Analytics Worker Pipeline │
                                                         │ - Real-Time Bot Fraud Scanner    │
                                                         │ - Storage: ClickHouse OLAP DB    │
                                                         └──────────────────────────────────┘
```

---

# 03. End-to-End Execution Flow Summary

1. **User requests short link creation (`POST /api/v1/urls`)**:
   - Request passes through WAF and ALB to API node.
   - API verifies JWT token, checks idempotency key in Redis, generates 64-bit Snowflake ID, encodes ID to 7-character Base62 string (`aB72x`).
   - Inserts row into PostgreSQL Shard.
   - Populates Redis cache key `url:aB72x` with target URL.
   - Returns `201 Created` with payload `{ "short_code": "aB72x", "short_url": "https://short.ly/aB72x" }`.

2. **End-user clicks short link (`GET /aB72x`)**:
   - Check CDN Edge Cache -> HIT returns `302 Found` in < 2ms.
   - If Edge Miss: ALB routes to API node. API checks Local RAM LRU -> Redis Cache.
   - If Redis Cache HIT: API publishes click event asynchronously to Kafka topic `click_events` in < 0.5ms and returns `302 Found` with `Location: https://target.com`.
   - Analytics Consumer Worker reads Kafka batch every 1,000ms and executes bulk insert into ClickHouse analytics storage.
