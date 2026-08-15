# Master Document: Architecture Evolution Guide

# 01. Learning Objective

By the end of this document, I should understand:
- How our URL Shortener system evolves across 6 distinct architectural generations.
- What specific engineering bottleneck forces us to upgrade from each generation to the next.
- How latency, throughput, storage capacity, and reliability change at each architectural stage.
- How to justify architectural upgrades in system design interviews.

---

# 02. Architectural Generations Summary

```text
Generation 1: Single-Node FastAPI + Single PostgreSQL
     │  (Bottleneck: DB CPU saturation at ~3,000 Read QPS)
     ▼
Generation 2: FastAPI + Redis Cache + Single PostgreSQL
     │  (Bottleneck: Single API Node CPU saturation at ~10,000 Read QPS)
     ▼
Generation 3: Load Balancer + API Node Cluster + Redis + PostgreSQL
     │  (Bottleneck: Database Write I/O & Read Bottleneck at 50,000 QPS)
     ▼
Generation 4: API Cluster + Redis + PostgreSQL Primary + Read Replicas
     │  (Bottleneck: Synchronous Click Logging Latency Spikes during redirects)
     ▼
Generation 5: API Cluster + Redis + DB Cluster + Apache Kafka + Analytics Workers
     │  (Bottleneck: Single DB Storage/RAM saturation at > 10 Billion URLs)
     ▼
Generation 6: Edge CDN/WAF + Load Balancer + API Cluster + Redis Cluster + DB Shards + Kafka + Analytics DB
```

---

# 03. Detailed Breakdown of Architectural Generations

## Generation 1 — Single-Node Baseline Monolith
- **Components**: Client -> FastAPI -> PostgreSQL.
- **Max Read Throughput**: ~3,000 QPS.
- **Limitation**: Every GET redirection requires disk I/O and B-Tree index lookup. Under traffic spikes, PostgreSQL CPU reaches 100%.

## Generation 2 — In-Memory Caching (Redis Introduced)
- **Components**: Client -> FastAPI -> Redis Cache -> PostgreSQL.
- **Max Read Throughput**: ~25,000 QPS.
- **Improvement**: 95%+ of redirection queries hit Redis in RAM (< 1ms latency).
- **Limitation**: A single Python FastAPI Uvicorn process is bounded by single CPU core execution.

## Generation 3 — Horizontal API Scaling (Load Balancer Introduced)
- **Components**: Client -> Nginx Load Balancer -> 4x API Nodes -> Redis -> PostgreSQL.
- **Max Read Throughput**: ~80,000 QPS.
- **Improvement**: API layer becomes completely stateless; request traffic is distributed across all CPU cores.
- **Limitation**: Read query traffic still hits single PostgreSQL instance on cache misses.

## Generation 4 — Database Read Scaling (Read Replicas Introduced)
- **Components**: API Cluster -> Redis -> PostgreSQL Primary (Writes) + 2x Read Replicas (Reads).
- **Max Read Throughput**: ~200,000 QPS.
- **Improvement**: Write traffic is isolated to Primary; read traffic scales horizontally across Replicas.
- **Limitation**: Synchronous click event persistence inside HTTP redirection requests slows down responses.

## Generation 5 — Asynchronous Event-Driven Pipeline (Kafka Introduced)
- **Components**: API Cluster -> Redis -> DB Primary/Replicas -> Apache Kafka -> Analytics Consumers.
- **Max Read Throughput**: ~500,000 QPS.
- **Improvement**: Redirection handler publishes click event to Kafka in < 1ms and returns `302 Found` immediately. Workers process analytics asynchronously.
- **Limitation**: Single PostgreSQL primary storage capacity reaches physical NVMe disk limit (2.5 TB).

## Generation 6 — Production Distributed Architecture (Sharding + CDN)
- **Components**: Cloudflare Edge CDN/WAF -> ALB -> API Cluster -> Redis Cluster -> Sharded DBs -> Kafka -> ClickHouse Analytics DB.
- **Max Read Throughput**: **> 2,000,000+ QPS**.
- **Result**: Global edge caching, multi-region database sharding, zero single point of failure (SPOF).
