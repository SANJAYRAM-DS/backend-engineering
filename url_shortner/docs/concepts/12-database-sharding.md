# Concept 12 — Database Sharding & Consistent Hashing

# 1. Why Shard?
When dataset size exceeds 5 Terabytes or write volume exceeds single-node disk limits, we partition data across multiple independent database nodes (**Shards**).

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

# 2. Consistent Hashing
Standard modulo hashing (`Hash(key) % N`) causes 99% of keys to remap to different nodes when adding or removing a shard.

**Consistent Hashing** maps nodes and keys onto a virtual $2^{32}$ hash ring. Adding a shard only remaps $1/N$ of keys, preventing massive cache invalidation storms.
