# 54 — System Bottleneck Analysis & Performance Tuning

## 1. Learning Objective
Identify hardware and software bottlenecks (CPU saturation, Memory pressure, Database Connection Exhaustion, Network I/O, Lock Contention) using empirical metrics.

---

## 2. Bottleneck Diagnostics Matrix

| Symptom | Root Cause | Diagnosis Command | Remediating Action |
| :--- | :--- | :--- | :--- |
| **p99 Latency > 200ms** | PostgreSQL connection pool saturation | `SELECT count(*) FROM pg_stat_activity;` | Increase connection pool or deploy PgBouncer. |
| **High CPU on API Node** | Single-threaded Uvicorn process bound | `top` / `htop` | Scale Uvicorn workers (`uvicorn --workers 4`). |
| **Redis Memory Eviction** | Missing TTL / No maxmemory policy | `redis-cli info memory` | Set `maxmemory-policy volatile-lru`. |
