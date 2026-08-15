# 46 & 47 — Structured JSON Logging & Correlation IDs

## 1. Learning Objective
Implement structured JSON logging with request-scoped `X-Correlation-ID` context propagation across microservices.

---

## 2. Structured JSON Log Output

```json
{
  "timestamp": "2026-08-15T09:00:00Z",
  "level": "INFO",
  "correlation_id": "c7b9e02c-14b2-4a25-8f64-90089a8123e4",
  "event": "url_redirect_resolved",
  "short_code": "aB72x",
  "latency_ms": 1.2,
  "cache_hit": true
}
```
