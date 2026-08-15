# 23 — Read vs Write Scaling Profiling

## 1. Learning Objective
Analyze read-heavy vs write-heavy operational characteristics and determine when vertical scaling ends and horizontal database read replication begins.

---

## 2. Read/Write Breakdown for URL Shortener

```text
Total System Traffic: 100%
  ├── 99% Read Operations (HTTP GET /{short_code} Redirections)
  └── 1% Write Operations (HTTP POST /api/v1/urls Creations)
```

Because read requests dominate traffic by $100:1$, we scale the database by decoupling write transactions from read lookups using PostgreSQL Primary-Replica streaming replication.
