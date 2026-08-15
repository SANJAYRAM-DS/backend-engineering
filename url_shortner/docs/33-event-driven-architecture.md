# 33 — Event-Driven Architecture & Loose Coupling

## 1. Learning Objective
Understand how Event-Driven Architecture (EDA) enables adding new business features (e.g., Geo-IP enrichment, fraud detection, email notifications) without modifying existing HTTP redirection services.

---

## 2. Decoupled Event Pipeline

```text
[ Redirection API Service ] ──(Publishes Event)──> [ Kafka Event Stream ]
                                                           │
        ┌───────────────────────────┬──────────────────────┴────────────────────┐
        ▼                           ▼                                           ▼
[ Analytics Worker ]      [ Fraud Detection Worker ]              [ Real-Time Dashboard Worker ]
 (DB Ingestion)           (Blocks Malicious IPs)                 (WebSockets Push)
```
