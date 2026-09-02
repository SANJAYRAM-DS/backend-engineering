# Patterns And Production Engineering

## Engineering Patterns

### Layered Architecture

Pattern: HTTP routes -> service layer -> repository layer -> database.

Where used: `src/api/v1/urls.py`, `src/services/url_service.py`, `src/repositories/url_repository.py`.

Why used: Keeps routing, business logic, and persistence separate.

Alternative: Put all logic in route handlers.

Trade-offs: More files and indirection, but much easier to test and modify.

### Repository Pattern

Pattern: Encapsulate database operations behind methods.

Where used: `URLRepository`.

Why used: Keeps SQLAlchemy query details out of service code.

Alternative: Call SQLAlchemy directly from `URLService`.

Trade-offs: Cleaner boundaries, but repository methods need careful transaction design.

### Dependency Injection

Pattern: Use FastAPI `Depends` to provide service dependencies.

Where used: `src/api/deps.py`.

Why used: Makes route functions small and tests easy to override.

Alternative: Global database sessions or manual object construction.

Trade-offs: Requires learning FastAPI dependency behavior.

### Cache-Aside

Pattern: Read cache first, fall back to database, then populate cache.

Where used: `URLService.resolve_url()`.

Why used: Redirects are read-heavy and benefit from low latency.

Alternative: Always read the database.

Trade-offs: Faster hot reads, but requires invalidation and stale-data thinking.

### Soft Delete

Pattern: Mark rows inactive instead of deleting them.

Where used: `URLRepository.deactivate_url()`.

Why used: Preserves historical records and prevents accidental reuse ambiguity.

Alternative: Hard delete rows.

Trade-offs: Safer audit/history, but queries must consistently filter inactive records.

### Middleware For Cross-Cutting Concerns

Pattern: Put rate limiting and idempotency outside route handlers.

Where used: `IdempotencyAndRateLimitMiddleware`.

Why used: These concerns apply broadly to requests.

Alternative: Implement checks in every route.

Trade-offs: Centralized behavior, but middleware can be tricky when reading/wrapping response bodies.

### Circuit Breaker

Pattern: Stop calling a failing dependency for a recovery window.

Where used: `src/services/circuit_breaker.py`.

Why used: Demonstrates resilience pattern.

Alternative: Retry every call normally.

Trade-offs: Protects the system during outages, but must be tuned and integrated carefully.

## Production Engineering Status

## Implemented

- Input validation through Pydantic.
- Basic SSRF protection against obvious localhost/private IP targets.
- Async database access.
- Database indexes for `short_code` and click-event lookups.
- Redis cache-aside with graceful fallback.
- Redis-backed sliding-window rate limiting.
- In-memory rate-limit fallback.
- Idempotency response cache for successful POST requests.
- Soft delete for URLs.
- Basic logging.
- Unit and integration tests.

## Partially Implemented

- Authentication: libraries and `User` model exist, but no auth flow.
- Authorization: no ownership checks exist.
- Observability: logging exists, but not structured JSON logs, metrics, or tracing.
- Docker: Compose file exists but appears malformed; Dockerfile is placeholder.
- Configuration: `.env` support exists, but production validation is minimal.
- Resilience: circuit breaker exists, but is not wired into Redis/database calls.
- Analytics: click count and click events exist, but no async pipeline.
- Error handling: API errors exist, but startup failures can be swallowed silently.

## Missing

- Alembic migrations.
- Auth endpoints and JWT verification.
- Role-based access control.
- Per-user URL ownership.
- Request correlation IDs.
- Metrics endpoint.
- Distributed tracing.
- Structured log fields.
- Kafka or any async analytics queue.
- Background workers.
- Cache stampede protection.
- Advanced hot-key protection.
- Real Docker production image.
- CI/CD pipeline.
- Security headers and strict CORS policy.
- URL malware/phishing scanning.
- Admin controls.
- Backup and disaster recovery procedures.
- Load testing.

