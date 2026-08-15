# Concept 09 — The Hot-Key Problem & Mitigation Strategies

# 1. The Hot-Key Problem Defined
When a single short URL goes viral (e.g., `short.ly/amazon-prime-day`), it generates **100,000 requests/second**.

Even with Redis, all 100,000 requests hit the **single Redis cluster node** hosting key `url:amazon-prime-day`, causing network card saturation and CPU throttling on that single node.

---

# 2. Mitigations

```text
[ 100,000 QPS Incoming Traffic ]
               │
               ▼
[ Local Worker In-Memory LRU Cache ] ──(Serves 95% of traffic locally)──> Latency < 0.01ms
               │
               ▼ (5% Traffic)
[ Redis Cluster ]
```

1. **Local Worker In-Memory LRU Cache**: Application worker processes store the top 50 viral keys in Python application RAM (`cachetools`). 95%+ of traffic never leaves application memory.
2. **Key Replication / Salting**: Duplicate hot key across Redis nodes as `url:key:1`, `url:key:2`, `url:key:3`. Pick random key suffix to balance load across cluster nodes.
