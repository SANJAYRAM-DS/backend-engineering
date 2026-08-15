# Concept 20 — Observability: Metrics, Logs & Tracing

# 1. Three Pillars of Observability

1. **Structured JSON Logs**: Log events as structured JSON with `correlation_id` across service boundaries.
2. **Prometheus Metrics**:
   - RED Metrics: Rate, Errors, Duration (p50, p95, p99 latency).
   - USE Metrics: Utilization, Saturation, Errors.
3. **Distributed Tracing (OpenTelemetry)**: Visualize request execution spans across API Router -> Redis -> PostgreSQL -> Kafka.
