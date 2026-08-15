# 26 — Database Sharding & Horizontal Partitioning

## 1. Learning Objective
Learn when a single PostgreSQL database reaches physical storage/RAM limits (e.g., > 10 Billion URLs, 5 TB data) and design a horizontal database sharding router.

---

## 2. Sharding Architecture

```text
                               [ API Shard Router ]
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 │                       │                       │
                 ▼                       ▼                       ▼
          [ Database Shard 0 ]    [ Database Shard 1 ]    [ Database Shard 2 ]
          (Hash % 3 == 0)         (Hash % 3 == 1)         (Hash % 3 == 2)
```

---

## 3. Shard Key Selection
Choosing `short_code` as the shard key ensures all lookup queries for a link target hit a single deterministic shard:
`Shard ID = Hash(short_code) % Total_Shards`
