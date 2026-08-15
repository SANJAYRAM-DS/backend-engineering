# Master Document: Distributed Systems Failure Handbook

# 01. Learning Objective

By the end of this document, I should understand:
- How every infrastructure component in our URL Shortener system can fail.
- How to detect, diagnose, recover, and mitigate component failures.
- How graceful degradation keeps our core URL redirection service running during infrastructure outages.

---

# 02. Centralized Failure Playbooks

## Playbook 1: Redis In-Memory Cache Outage
- **Failure Scenario**: Redis node crashes or network partition disconnects Redis.
- **System Impact**: 100% cache misses. Read requests fall back to PostgreSQL.
- **Detection**: Prometheus alert `redis_up == 0` or application log `redis.exceptions.ConnectionError`.
- **Automatic Fallback Strategy**: Application catches Redis connection exception, executes Circuit Breaker to prevent thread exhaustion, and queries PostgreSQL directly.
- **Recovery Action**: Restart Redis node (`docker start url_shortener_redis`). Upon reconnection, Circuit Breaker moves to `HALF-OPEN` and repopulates cache.

---

## Playbook 2: PostgreSQL Primary Node Failure
- **Failure Scenario**: Primary database container/server crashes due to hardware failure or disk full error.
- **System Impact**: New short URL creations (`POST /api/v1/urls`) fail with HTTP 500.
- **Detection**: `pg_isready` health check fails; application log `asyncpg.exceptions.CannotConnectNowError`.
- **Automatic Fallback Strategy**: **Active short URL redirections continue working seamlessly from Redis Cache!**
- **Recovery Action**: Failover manager (Patroni / AWS Multi-AZ) promotes Read Replica 1 to new Primary node.

---

## Playbook 3: Apache Kafka Broker Failure
- **Failure Scenario**: Kafka broker dies or consumer lag balloons due to network outage.
- **System Impact**: Click telemetry cannot be published synchronously to Kafka topic.
- **Detection**: `aiokafka.errors.KafkaConnectionError` or Prometheus metric `kafka_consumer_lag > 50000`.
- **Automatic Fallback Strategy**: API Producer catches Kafka publish timeout, buffers click event to local Redis queue (`RPUSH analytics_buffer`), and returns HTTP 302 to user without delay.
- **Recovery Action**: Upon Kafka restoration, background worker flushes Redis buffer back into Kafka topic.

---

## Playbook 4: Database Read Replica Lag Spikes
- **Failure Scenario**: High write volume causes WAL replication lag on Read Replicas to exceed 10 seconds.
- **System Impact**: User creates short link and immediately clicks it, resulting in temporary `404 Not Found` if hit on replica.
- **Detection**: `SELECT pg_last_wal_replay_lsn() - pg_last_wal_receive_lsn();` on replica.
- **Mitigation Strategy**: Implement "Read-After-Write Consistency": route user's reads to Primary node or serve from synchronous Redis cache for 5 seconds post-creation.
