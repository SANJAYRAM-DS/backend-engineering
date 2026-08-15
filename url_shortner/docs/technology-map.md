# Master Document: Problem-to-Technology Decision Map

# 01. Learning Objective

By the end of this document, I should understand:
- How every major technology choice maps directly to a specific backend engineering problem.
- Why we selected specific tools over industry alternatives.
- The architectural trade-offs associated with each technology.

---

# 02. Problem-to-Technology Matrix

| Backend Problem / Challenge | Technology Choice | Why Choice Was Made | Alternatives Considered | Trade-offs & Operational Cost |
| :--- | :--- | :--- | :--- | :--- |
| **High-Throughput Async API Routing** | **FastAPI + AsyncIO** | Native async/await event loop, strict Pydantic payload validation, high productivity. | Express.js, Go (Gin), Spring Boot | Single-threaded CPU limits per worker; scale horizontally via Uvicorn workers. |
| **ACID Compliant Data Persistence** | **PostgreSQL 16** | Strong data integrity, B-Tree & Partial indexing, JSONB support, robust replication ecosystem. | MySQL, MongoDB, DynamoDB | Strict migrations required; requires connection pool tuning (asyncpg / PgBouncer). |
| **Sub-Millisecond Read Latency** | **Redis 7** | In-memory key-value lookups (< 1ms), rich data structures, native TTL key eviction. | Memcached, KeyDB | Data volatile in RAM; requires cache-aside invalidation logic in application. |
| **Decoupled Async Telemetry Processing** | **Apache Kafka** | Distributed commit log, high throughput, pub/sub consumer groups, event replay capability. | RabbitMQ, AWS SQS, NATS | Operational overhead (KRaft/ZooKeeper management, partition sizing). |
| **Distributed Unique ID Generation** | **Twitter Snowflake** | 64-bit time-ordered integer IDs, zero database lock coordination, 4,096 IDs/ms per worker. | UUIDv4, Auto-increment BIGSERIAL | Requires worker ID assignment per API instance. |
| **Abuse & Rate Limiting Defense** | **Redis Sliding Window Log** | Precise timestamp tracking per IP using Redis Sorted Sets; immune to boundary burst attacks. | Fixed Window, Token Bucket | Memory usage overhead for storing timestamp elements in sorted sets. |
| **High Load & Performance Profiling** | **Locust** | Python-based scriptable load testing tool; simulates thousands of concurrent HTTP clients. | k6, Apache JMeter, wrk | Python runner process memory consumption under heavy client load. |
