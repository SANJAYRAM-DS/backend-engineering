# Concepts Connected To Real Code

## Concept: FastAPI Routing

Where it appears: `src/main.py`, `src/api/v1/urls.py`.

Why the project uses it: The app needs HTTP endpoints for URL creation, analytics, deletion, health-like documentation, and redirect behavior.

How it works: Decorators such as `@router.post("")`, `@router.get(...)`, and `@app.get("/{short_code}")` bind Python functions to HTTP routes.

Important files: `src/main.py`, `src/api/v1/urls.py`.

What to learn: Route matching, path parameters, status codes, response models, redirect responses.

Exercise: Add `GET /api/v1/urls/{short_code}` to return URL metadata without analytics.

## Concept: Dependency Injection

Where it appears: `src/api/deps.py`, route function parameters.

Why the project uses it: Routes should not manually create database sessions, Redis clients, or service instances.

How it works: FastAPI calls dependencies declared with `Depends(...)`. `get_url_service()` receives a DB session and Redis client, then returns `URLService`.

Important files: `src/api/deps.py`, `tests/conftest.py`.

What to learn: `Depends`, nested dependencies, test overrides.

Exercise: Override `get_url_service()` in a test with a fake service.

## Concept: Pydantic Validation

Where it appears: `src/schemas/url.py`.

Why the project uses it: The API must reject malformed URLs and unsafe targets before they reach business logic.

How it works: `URLCreateRequest` validates `original_url`, `custom_alias`, and optional `expires_at`.

Important files: `src/schemas/url.py`, `tests/unit/test_url_validation.py`.

What to learn: field validators, validation error responses, schema examples.

Exercise: Reject custom aliases equal to reserved route names such as `docs`, `openapi.json`, and `api`.

## Concept: Async SQLAlchemy Session Management

Where it appears: `src/db/session.py`.

Why the project uses it: FastAPI can handle concurrent requests efficiently when I/O operations are awaited.

How it works: `create_async_engine()` creates a connection engine. `async_sessionmaker()` creates sessions. `get_db()` yields one session per request.

Important files: `src/db/session.py`, `src/repositories/url_repository.py`.

What to learn: async sessions, connection pools, commits, rollback implications.

Exercise: Add rollback handling to repository write failures.

## Concept: ORM Models

Where it appears: `src/db/models.py`.

Why the project uses it: Python classes define relational tables and indexes.

How it works: `URL`, `ClickEvent`, and `User` inherit from SQLAlchemy `Base`.

Important files: `src/db/models.py`.

What to learn: primary keys, indexes, unique constraints, nullable columns, timestamps.

Exercise: Add a `last_accessed_at` column to `URL` and update it during redirect.

## Concept: Repository Pattern

Where it appears: `src/repositories/url_repository.py`.

Why the project uses it: SQL queries are isolated from business rules.

How it works: `URLRepository` accepts an `AsyncSession` and exposes methods such as `get_by_short_code`, `create_url`, and `deactivate_url`.

Important files: `src/repositories/url_repository.py`.

What to learn: query encapsulation, transaction boundaries, persistence isolation.

Exercise: Add `get_click_events(short_code, limit)` and expose it through a new analytics-detail endpoint.

## Concept: Service Layer

Where it appears: `src/services/url_service.py`.

Why the project uses it: URL creation, redirect resolution, cache management, and telemetry are business workflows that span multiple dependencies.

How it works: The service coordinates repository calls, Redis operations, ID generation, expiration checks, and response construction.

Important files: `src/services/url_service.py`.

What to learn: orchestration logic, error handling, separation of concerns.

Exercise: Move expiration checking into a helper method and add tests.

## Concept: Snowflake ID Generation

Where it appears: `src/services/snowflake.py`.

Why the project uses it: Generated short codes need unique high-throughput numeric input without relying on a central database counter.

How it works: The generator combines timestamp, datacenter ID, worker ID, and sequence bits into a sortable integer.

Important files: `src/services/snowflake.py`, `tests/unit/test_snowflake.py`.

What to learn: bit shifts, sequence rollover, clock rollback, worker coordination.

Exercise: Decode a generated ID into timestamp, datacenter, worker, and sequence components.

## Concept: Base62 Encoding

Where it appears: `src/services/base62.py`.

Why the project uses it: Numeric IDs need compact URL-safe string representation.

How it works: Repeated division by 62 maps remainders to `0-9a-zA-Z`.

Important files: `src/services/base62.py`, `tests/unit/test_base62.py`.

What to learn: base conversion, URL-safe alphabets, reversibility.

Exercise: Add property-style tests that encode and decode many random integers.

## Concept: Redis Cache-Aside

Where it appears: `src/core/redis.py`, `src/services/url_service.py`.

Why the project uses it: Redirects are read-heavy and should avoid database lookups when possible.

How it works: `resolve_url()` checks `url:{short_code}` in Redis. On miss, it reads from DB and then writes Redis with a TTL.

Important files: `src/core/redis.py`, `src/services/url_service.py`.

What to learn: cache hit, cache miss, TTL, invalidation, degraded mode.

Exercise: Add a test using a fake Redis client to prove cache hit avoids repository lookup.

## Concept: Sliding-Window Rate Limiting

Where it appears: `src/api/middleware.py`.

Why the project uses it: It limits abuse by IP address before routes run.

How it works: Redis sorted sets store request timestamps per client IP. Old timestamps are removed; if count exceeds 100 in 60 seconds, the request receives `429`.

Important files: `src/api/middleware.py`.

What to learn: middleware lifecycle, Redis sorted sets, atomic pipelines, distributed consistency.

Exercise: Make limit values configurable through `Settings`.

## Concept: Idempotency

Where it appears: `src/api/middleware.py`.

Why the project uses it: Clients can safely retry POST requests with the same `Idempotency-Key`.

How it works: Successful `201` POST responses are cached in Redis for 24 hours and replayed for the same key.

Important files: `src/api/middleware.py`.

What to learn: retry safety, request fingerprinting, replay risk, response caching.

Exercise: Include request path and body hash in the idempotency cache key.

## Concept: Circuit Breaker

Where it appears: `src/services/circuit_breaker.py`.

Why the project uses it: Circuit breakers prevent repeated calls to failing dependencies.

How it works: After a failure threshold, the breaker opens and rejects calls until recovery time passes. Then it enters half-open mode.

Important files: `src/services/circuit_breaker.py`, `tests/unit/test_circuit_breaker.py`.

What to learn: closed/open/half-open states, fail-fast behavior, recovery probes.

Exercise: Wrap Redis reads in a circuit breaker and compare behavior during Redis failure.

