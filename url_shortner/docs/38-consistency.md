# 38 — Consistency Models & Eventual Consistency Realities

## 1. Learning Objective
Compare Strong Consistency vs Eventual Consistency in distributed systems.

---

## 2. Trade-offs in URL Shortener

- **URL Creation (Strong Consistency)**: Requires strong ACID checks to guarantee custom aliases are strictly unique globally.
- **Analytics Click Aggregation (Eventual Consistency)**: Click counters can lag by 1–5 seconds while queued in Kafka without impacting user redirection experience.
