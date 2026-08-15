# 00 — Master Project Roadmap & Curriculum Architecture

# 01. Learning Objective

By the end of this document, I should understand:
- What the complete 64-module distributed systems curriculum covers.
- Why we build the system starting from a single node and evolving step-by-step.
- How each module depends on previous modules in a clear learning dependency graph.
- When architectural complexity (Redis, Kafka, Sharding, Replicas) should be introduced.
- Trade-offs between simple monolithic designs vs distributed microservices.
- How to navigate this repository as a self-guided learning course.
- How to evaluate my own learning using checkpoints and interview questions.

---

# 02. Prerequisites

Before starting this course, I should understand:
- Basic Python programming (variables, functions, classes, async/await basics).
- Basic SQL syntax (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
- Basic HTTP protocol concepts (GET, POST, Status Codes 200, 302, 404, 500).
- Terminal/CLI usage and Docker fundamentals.

If you need refresher material on these concepts, review:
- [01-problem-understanding.md](file:///e:/backend_engineering/url_shortner/docs/01-problem-understanding.md)
- [02-requirements.md](file:///e:/backend_engineering/url_shortner/docs/02-requirements.md)

---

# 03. Problem We Are Solving

Building production backend systems is difficult because standard computer science tutorials show only trivial "Hello World" examples or jump straight to complex microservices without explaining **why** the complexity is necessary.

```text
Trivial Tutorials:
[ Client ] ──> [ API ] ──> [ SQLite ]  (Unscalable, unrealistic)

Over-Engineered Tutorials:
[ Client ] ──> [ Kubernetes ] ──> [ Service Mesh ] ──> [ Kafka ] ──> [ Redis Cluster ] ──> [ Cassandra ] (Confusing, overwhelming)
```

We need a structured curriculum that bridges this gap by starting with the simplest working system and letting real-world scaling bottlenecks force us to introduce each distributed systems component.

---

# 04. Why This Problem Exists

In real engineering teams:
1. **Premature Optimization** leads to wasted engineering capital, high cloud infrastructure bills, and nightmare debugging.
2. **Under-Engineering** leads to database crashes under traffic spikes, data loss, and breaking SLAs.

By learning **Architectural Evolution**, you gain the principal software architect mindset: introducing complexity **only** when forced by measurable bottlenecks.

---

# 05. Concept / Theory

### The Progressive Architecture Evolution Flow

$$\text{Version 1: Single-Node Monolith} \longrightarrow \text{Version 2: In-Memory Caching} \longrightarrow \text{Version 3: Read Replicas} \longrightarrow \text{Version 4: Async Event Streaming} \longrightarrow \text{Version 5: Distributed Sharding & Production Architecture}$$

```text
V1: Client ──> API ──> PostgreSQL
V2: Client ──> API ──> Redis ──> PostgreSQL
V3: Client ──> API ──> Redis ──> DB Primary ──> DB Replicas
V4: Client ──> API ──> Redis ──> DB Primary ──> Kafka ──> Analytics Workers
V5: Client ──> WAF/CDN ──> Load Balancer ──> API Cluster ──> Redis Cluster ──> DB Shards ──> Kafka ──> Analytics DB
```

---

# 06. Master Document Dependency Graph & Curriculum Index

### Master Documents
- 📄 [00-roadmap.md](file:///e:/backend_engineering/url_shortner/docs/00-roadmap.md) — Master Learning Roadmap
- 📄 [architecture-evolution.md](file:///e:/backend_engineering/url_shortner/docs/architecture-evolution.md) — V1 to Production Architectural Evolution
- 📄 [technology-map.md](file:///e:/backend_engineering/url_shortner/docs/technology-map.md) — Problem-to-Technology Decision Matrix
- 📄 [failure-handbook.md](file:///e:/backend_engineering/url_shortner/docs/failure-handbook.md) — Centralized Distributed Failure Handbook
- 📄 [interview-preparation.md](file:///e:/backend_engineering/url_shortner/docs/interview-preparation.md) — Master System Design Interview Question Bank
- 📄 [final-system-design.md](file:///e:/backend_engineering/url_shortner/docs/final-system-design.md) — Master Production Architecture Blueprint

### Module Tutorials (01 — 63)
- 📄 [01-problem-understanding.md](file:///e:/backend_engineering/url_shortner/docs/01-problem-understanding.md) — HTTP Redirect Mechanics (301 vs 302)
- 📄 [02-requirements.md](file:///e:/backend_engineering/url_shortner/docs/02-requirements.md) — Requirements & Capacity Estimation Math
- 📄 [03-system-design.md](file:///e:/backend_engineering/url_shortner/docs/03-system-design.md) — High-Level Architecture & Clean Layering
- 📄 [04-api-design.md](file:///e:/backend_engineering/url_shortner/docs/04-api-design.md) — RESTful API Contracts & OpenAPI Specs
- 📄 [05-database-design.md](file:///e:/backend_engineering/url_shortner/docs/05-database-design.md) — Schema Design, B-Tree Indexes & Connection Pools
- 📄 [06-project-setup.md](file:///e:/backend_engineering/url_shortner/docs/06-project-setup.md) — Hands-On Monolith Setup & Code Guide
- 📄 [11-base62.md](file:///e:/backend_engineering/url_shortner/docs/11-base62.md) — Base62 Encoding from First Principles
- 📄 [17-redis.md](file:///e:/backend_engineering/url_shortner/docs/17-redis.md) — In-Memory Caching & Redis Fundamentals
- 📄 [18-caching.md](file:///e:/backend_engineering/url_shortner/docs/18-caching.md) — Cache-Aside Implementation
- 📄 [21-rate-limiting.md](file:///e:/backend_engineering/url_shortner/docs/21-rate-limiting.md) — Distributed Sliding Window Rate Limiting
- 📄 [24-database-replication.md](file:///e:/backend_engineering/url_shortner/docs/24-database-replication.md) — PostgreSQL Primary/Replica Setup
- 📄 [29-distributed-ids.md](file:///e:/backend_engineering/url_shortner/docs/29-distributed-ids.md) — Twitter Snowflake ID Generator
- 📄 [32-kafka.md](file:///e:/backend_engineering/url_shortner/docs/32-kafka.md) — Apache Kafka Integration & Delivery Semantics
- 📄 [41-retries.md](file:///e:/backend_engineering/url_shortner/docs/41-retries.md) — Exponential Backoff & Jitter
- 📄 [43-circuit-breaker.md](file:///e:/backend_engineering/url_shortner/docs/43-circuit-breaker.md) — Circuit Breakers
- 📄 [44-idempotency.md](file:///e:/backend_engineering/url_shortner/docs/44-idempotency.md) — Idempotency Keys & Safe Retries
- 📄 [53-load-testing.md](file:///e:/backend_engineering/url_shortner/docs/53-load-testing.md) — Performance Benchmarking with Locust
- 📄 [63-what-i-learned.md](file:///e:/backend_engineering/url_shortner/docs/63-what-i-learned.md) — Master Learning Summary

---

# 33. Learning Checkpoint

Before proceeding, I should be able to explain:
- [ ] What problem each architectural tier solves.
- [ ] Why starting simple is essential for engineering projects.
- [ ] How to trace dependencies between docs.

---

# 34. Completion Checklist

- [ ] Reviewed `00-roadmap.md`.
- [ ] Inspected master document list.
- [ ] Understood architectural evolution flow.

---

# 35. What Comes Next

Next document: [docs/architecture-evolution.md](file:///e:/backend_engineering/url_shortner/docs/architecture-evolution.md)
