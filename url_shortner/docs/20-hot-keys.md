# 20 — Mitigating the Hot-Key Problem

## 1. Learning Objective
Diagnose and solve the **Hot-Key Bottleneck** when a viral short link (e.g., `short.ly/superbowl-deal`) receives 100,000 requests per second, overloading a single Redis cluster node.

---

## 2. Hot-Key Mitigation Patterns

```text
                                [ 100,000 QPS Incoming Requests ]
                                                │
                                                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                          LOCAL IN-MEMORY LRU CACHE                            │
│                     (Python Application Worker Memory)                        │
│                     - Holds top 50 viral keys in RAM                          │
│                     - Latency: < 0.001 ms                                     │
└──────────────────────────────────────┬────────────────────────────────────────┘
                                       │
                                       │ 95% Traffic Handled Locally
                                       v
┌───────────────────────────────────────────────────────────────────────────────┐
│                                REDIS CLUSTER                                  │
│                       (Secondary Shared Cache Node)                           │
└───────────────────────────────────────────────────────────────────────────────┘
```

1. **Local Worker In-Memory LRU Cache**: Use `cachetools` LRU cache in API worker process RAM to serve viral hot keys without network trips to Redis.
2. **Key Replication / Salting**: Duplicate hot key across Redis shards as `url:aB72x:1`, `url:aB72x:2`, `url:aB72x:3`. Pick random shard suffix per request to distribute network load.
