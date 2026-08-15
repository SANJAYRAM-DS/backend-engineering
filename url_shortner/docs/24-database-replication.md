# 24 — Database Replication Architecture (Primary / Read Replicas)

## 1. Learning Objective
Design a multi-node PostgreSQL replication cluster with one Primary (Writer) node and multiple Read Replicas (Readers).

---

## 2. Replication Architecture

```text
                        [ API Write Traffic ]
                                 │
                                 ▼
                     [ PostgreSQL Primary Node ]
                       (Handles INSERT / UPDATE)
                                 │
                 ┌───────────────┴───────────────┐
                 │ Write-Ahead Log (WAL) Stream  │
                 ▼                               ▼
       [ PostgreSQL Replica 1 ]       [ PostgreSQL Replica 2 ]
          (Handles GET Reads)            (Handles GET Reads)
```

---

## 3. Asynchronous vs Synchronous Replication
- **Asynchronous Replication**: Primary commits transactions locally immediately, then streams Write-Ahead Logs (WAL) to replicas. Ultra-fast write latency, but introduces **Replication Lag**.
- **Synchronous Replication**: Primary waits for at least one replica to write WAL log to disk before responding `COMMIT`. Zero data loss, higher write latency.
