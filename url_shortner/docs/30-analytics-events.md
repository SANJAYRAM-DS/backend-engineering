# 30 — Asynchronous Analytics Bottleneck Analysis

## 1. Learning Objective
Identify why synchronous click telemetry database inserts block HTTP redirection response times and justify introducing an event-driven asynchronous processing pipeline.

---

## 2. The Problem with Synchronous Click Logging

```text
Synchronous Flow (Slow):
GET /aB72x ──> [ Read DB/Cache ] ──> [ INSERT INTO click_events (DB Disk I/O) ] ──> [ 302 Redirect ]
                                     ▲
                                     └─ Adds 20ms - 50ms latency to every redirect!
```

By decoupling redirection from click persistence via message queues, redirection latency drops back down to < 5ms.
