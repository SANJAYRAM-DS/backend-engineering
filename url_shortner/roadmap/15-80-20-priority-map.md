# 80/20 Priority Map

## Must Learn

### FastAPI Request Lifecycle

Why: Every feature enters through FastAPI.

Study: `src/main.py`, `src/api/v1/urls.py`, `src/api/deps.py`.

Outcome: You can explain how a request reaches `URLService`.

### Service And Repository Layers

Why: This is the core architecture.

Study: `src/services/url_service.py`, `src/repositories/url_repository.py`.

Outcome: You know where business rules and SQL operations belong.

### Pydantic Validation

Why: Input validation is central to API safety.

Study: `src/schemas/url.py`, `tests/unit/test_url_validation.py`.

Outcome: You can safely add request fields and validation rules.

### Async Database Access

Why: Persistence is required for all core behavior.

Study: `src/db/session.py`, `src/db/models.py`, `src/repositories/url_repository.py`.

Outcome: You can add a model field, query it, update it, and test it.

### URL Creation And Redirect Flows

Why: These are the product.

Study: `src/services/url_service.py`, `tests/integration/test_url_api.py`.

Outcome: You can trace and modify the two main workflows.

## Should Learn

### Snowflake And Base62

Why: They explain generated short codes.

Study: `src/services/snowflake.py`, `src/services/base62.py`.

Outcome: You can reason about uniqueness, code length, and collisions.

### Redis Cache-Aside

Why: It is the main performance optimization.

Study: `src/core/redis.py`, `src/services/url_service.py`.

Outcome: You understand cache hit, miss, TTL, fallback, and invalidation.

### Testing With Dependency Overrides

Why: It makes backend changes safe.

Study: `tests/conftest.py`, `tests/integration/test_url_api.py`.

Outcome: You can test FastAPI behavior without running external services.

### Middleware

Why: It handles cross-cutting request behavior.

Study: `src/api/middleware.py`.

Outcome: You understand rate limiting and idempotency.

## Nice To Know

### Circuit Breaker

Why: Good resilience concept, but not wired into main flows.

Study: `src/services/circuit_breaker.py`.

Outcome: You understand fail-fast dependency protection.

### Docker Compose

Why: Local service orchestration matters, but current file likely needs fixing.

Study: `docker-compose.yml`.

Outcome: You can run PostgreSQL and Redis locally once corrected.

### Logging

Why: Useful for debugging, but current setup is basic.

Study: `src/core/logging.py`.

Outcome: You can improve logs for production debugging.

## Advanced

### Authentication And Authorization

Why: Needed for real multi-user production use.

Study: `src/db/models.py`, `requirements.txt`.

Outcome: You can build user login, JWT validation, and ownership rules.

### Migrations

Why: Production databases should not rely on `create_all`.

Study: `src/db/models.py`; then add Alembic.

Outcome: You can evolve schema safely.

### Async Analytics

Why: Redirect writes become a bottleneck at scale.

Study: `src/services/url_service.py`, then design queue/worker architecture.

Outcome: You can decouple telemetry from redirect latency.

### Observability

Why: Production systems need metrics, logs, and traces.

Study: `src/core/logging.py`, middleware, service methods.

Outcome: You can identify errors, latency, traffic, cache hit rate, and bottlenecks.

### Distributed Systems Scaling

Why: The README's full architecture depends on it.

Study: after mastering the code, then read `docs/`.

Outcome: You can discuss sharding, replication, hot keys, load balancing, event streaming, and disaster recovery.

