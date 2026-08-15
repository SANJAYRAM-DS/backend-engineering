# 27 — Consistent Hashing Algorithms

## 1. Learning Objective
Understand why modular hashing (`Hash(key) % N`) causes massive cache/shard remapping when adding or removing nodes, and implement **Consistent Hashing** using a Virtual Node Hash Ring.

---

## 2. Hash Ring Topology

```text
                        [ Node A (0°) ]
                              │
             [ Key 3 ]        │        [ Key 1 ]
                 \            │           /
                  \           │          /
     [ Node C (240°) ] ───────┼─────── [ Node B (120°) ]
                  /           │          \
                 /            │           \
             [ Key 4 ]        │        [ Key 2 ]
```

When Node B fails, only keys mapped to Node B are reassigned to Node C. 99% of all other keys remain mapped to their original nodes without cache invalidation storms.
