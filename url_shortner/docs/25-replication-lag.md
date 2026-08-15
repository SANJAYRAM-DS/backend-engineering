# 25 — Handling Replication Lag & Read-After-Write Consistency

## 1. Learning Objective
Solve the **Read-After-Write Inconsistency** problem where a user creates a short URL, immediately clicks it, and receives a `404 Not Found` because the Read Replica hasn't received the WAL log yet.

---

## 2. Mitigation Strategies

1. **Sticky Session / Pinning to Primary**: After a user creates a link, force their client reads to query the **Primary Node** for 5 seconds before switching back to Read Replicas.
2. **Read from Cache First**: Since Redis cache is updated synchronously upon creation, cache hits bypass replication lag entirely.
