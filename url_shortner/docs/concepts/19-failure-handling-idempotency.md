# Concept 19 — Distributed Resilience & Idempotency

# 1. Resilience Patterns

- **Timeouts**: Socket connection timeouts prevent thread exhaustion during downstream latency spikes.
- **Exponential Backoff with Jitter**: Spreads retries randomly over time to prevent **Retry Storms** against recovering databases.
- **Circuit Breakers**: `CLOSED -> OPEN -> HALF-OPEN` state machine fails fast when Redis or external APIs die.

---

# 2. Idempotency Keys
If a client sends `POST /api/v1/urls`, the server processes it, but the response is lost over the network:

Client retries request $\longrightarrow$ duplicate link generated!

**Idempotency Header (`Idempotency-Key: 7b9e02c1...`)**:
API checks Redis key `idempotency:7b9e02c1`. If found, returns cached 201 response immediately without duplicate database insertion.
