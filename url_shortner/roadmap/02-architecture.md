# Reconstructed Architecture

## Actual Architecture

```text
User / HTTP Client
      |
FastAPI Application
      |
Middleware
  - rate limiting
  - idempotency for POST
      |
API Routes
  - src/api/v1/urls.py
  - src/main.py redirect route
      |
Dependency Injection
  - database session
  - optional Redis client
      |
URLService
  - short-code generation
  - alias conflict checks
  - cache coordination
  - redirect resolution
  - analytics writes
      |
URLRepository
  - SQLAlchemy queries
  - transaction commits
      |
PostgreSQL / SQLite in tests
      |
Optional Redis
  - URL cache
  - rate-limit sorted sets
  - idempotency response cache
```

## Component Responsibilities

### FastAPI App

What it does: Owns app startup, shutdown, middleware registration, routing, and OpenAPI generation.

Why it exists: It is the HTTP boundary between users and application code.

How it works: `src/main.py` creates `app`, registers `IdempotencyAndRateLimitMiddleware`, includes `/api/v1` routes, and defines the redirect route.

What depends on it: Tests import `app`; uvicorn runs `src.main:app`.

### Middleware

What it does: Applies request-wide rate limiting and idempotency.

Why it exists: These concerns should apply before route handlers run.

How it works: `src/api/middleware.py` uses Redis sorted sets for sliding-window rate limiting. If Redis is unavailable, it uses an in-memory dictionary. For POST requests with `Idempotency-Key`, Redis stores and replays successful responses.

What depends on it: All HTTP requests pass through it.

### API Routes

What they do: Expose HTTP operations.

Why they exist: They keep HTTP-specific concerns separate from business rules.

How they work: Route functions receive validated Pydantic models and injected services, then call `URLService`.

What depends on them: API clients and integration tests.

### Dependency Injection

What it does: Creates per-request service objects with a database session and optional Redis client.

Why it exists: It makes routes testable and avoids direct construction in every handler.

How it works: `get_url_service()` depends on `get_db()` and `get_redis_dep()`.

What depends on it: All URL routes and the redirect route.

### URLService

What it does: Coordinates business logic.

Why it exists: It keeps route handlers small and prevents SQL details from leaking into the API layer.

How it works: It generates or validates short codes, calls repository methods, updates Redis cache entries, handles expiration checks, and writes telemetry.

What depends on it: API routes and redirect handler.

### URLRepository

What it does: Encapsulates database access.

Why it exists: It separates persistence operations from business rules.

How it works: It uses SQLAlchemy async sessions to select, insert, update, and commit.

What depends on it: `URLService`.

### Database Models

What they do: Define persistent data shape.

Why they exist: SQLAlchemy needs models to map Python objects to database tables.

How they work: `User`, `URL`, and `ClickEvent` inherit from `Base`.

What depends on them: Repository queries, startup table creation, and test fixtures.

### Redis Integration

What it does: Provides optional low-latency cache and middleware storage.

Why it exists: URL shorteners are read-heavy; redirects should avoid database lookups where possible.

How it works: `get_redis_client()` lazily connects and returns `None` if Redis is unavailable.

What depends on it: `URLService`, middleware, dependency injection, shutdown cleanup.

## Important Boundaries

- HTTP boundary: `src/main.py`, `src/api/v1/urls.py`.
- Validation boundary: `src/schemas/url.py`.
- Business boundary: `src/services/url_service.py`.
- Persistence boundary: `src/repositories/url_repository.py`.
- Infrastructure boundary: `src/core/config.py`, `src/core/redis.py`, `src/db/session.py`.
- Test boundary: `tests/conftest.py` overrides production dependencies.

## Critical Execution Paths

1. URL creation path: validate request -> generate code -> write DB -> populate cache.
2. Redirect path: rate limit -> cache lookup -> DB fallback -> telemetry writes -> redirect.
3. Deletion path: lookup -> soft delete -> cache invalidation.
4. Testing path: override DB and Redis dependencies -> exercise app through HTTPX ASGI transport.

