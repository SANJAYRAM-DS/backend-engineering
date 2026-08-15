# 22 — Database Optimization & Advanced Indexing

## 1. Learning Objective
Master database query tuning, index types (B-Tree, Hash, BRIN, Partial Indexes), covering indexes, and execution plan analysis.

---

## 2. Advanced Indexing Concepts

### Partial Index
Indexes only active short URLs, saving index RAM footprint by 40%:
```sql
CREATE INDEX idx_urls_active ON urls(short_code) WHERE is_active = TRUE;
```

### Covering Index (`INCLUDE` Clause)
Allows PostgreSQL to perform an **Index-Only Scan** without touching the disk heap table pages:
```sql
CREATE UNIQUE INDEX idx_urls_cover ON urls(short_code) INCLUDE (original_url, expires_at);
```
