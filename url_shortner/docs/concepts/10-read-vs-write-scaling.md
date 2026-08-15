# Concept 10 — Read vs Write Scaling Profiling

# 1. Read-Heavy System Profiling

```text
URL Shortener Workload Breakdown:
Reads (GET Redirections):  ████████████████████████████████ 99.9%
Writes (POST Creation):   █ 0.1%
```

Because read operations dominate traffic by $100:1$ to $1000:1$, write optimization and read scaling must be decoupled:
- **Write Path**: Optimized for data durability and strict primary key uniqueness.
- **Read Path**: Scaled aggressively via Edge CDNs, In-Memory Redis Caching, and PostgreSQL Read Replicas.
