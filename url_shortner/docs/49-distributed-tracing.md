# 49 — Distributed Tracing with OpenTelemetry & Jaeger

## 1. Learning Objective
Trace request execution spans end-to-end across API Router -> Redis Cache -> PostgreSQL DB -> Kafka Producer.

---

## 2. Distributed Span Execution Visualization

```text
[ Client GET /aB72x ] ──────────────────────────────────────────────────────────┐ (Total: 4.5ms)
    ├── [ Span: API Route Processing ] ──────────────────────┐ (0.2ms)          │
    ├── [ Span: Redis Get Key "url:aB72x" ] ─────────┐ (0.6ms)│                 │
    └── [ Span: Kafka Publish Event ] ──────────┐ (2.8ms)    │                 │
```
