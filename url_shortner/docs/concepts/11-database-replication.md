# Concept 11 — Database Replication & Replication Lag

# 1. Primary / Read Replica Architecture

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

- **Primary Node**: Handles all write transactions (`INSERT`, `UPDATE`, `DELETE`). Single source of truth.
- **Read Replicas**: Read-only mirror nodes. Scaled horizontally to handle high read volume.

---

# 2. Replication Lag & Read-After-Write Consistency
Because replication is asynchronous, WAL logs take a few milliseconds to reach replicas.

If a user creates `short.ly/aB72x` and clicks it 1ms later, querying a Read Replica might return `404 Not Found` (Replication Lag).

### Solution: Sticky Session Pinning
After creating a link, route the user's reads to the **Primary Node** or **Redis Cache** for 5 seconds before switching back to Read Replicas.
