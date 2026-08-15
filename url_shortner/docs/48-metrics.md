# 48 — Prometheus Metrics & Grafana Dashboards

## 1. Learning Objective
Expose Prometheus metrics endpoints (`/metrics`) to measure RED metrics (Rate, Errors, Duration) and USE metrics (Utilization, Saturation, Errors).

---

## 2. Core Prometheus Metrics

- `url_redirect_requests_total{status="302"}`: Total counter of successful redirections.
- `url_redirect_latency_seconds_bucket`: Histogram of p50, p95, p99 redirection latencies.
- `redis_cache_hits_total` / `redis_cache_misses_total`: Cache hit ratio calculator.
