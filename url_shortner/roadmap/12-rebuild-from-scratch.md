# Rebuild From Scratch Roadmap

Do not copy source code. Rebuild behavior from understanding.

## Milestone 1 - Minimal Architecture

What to build: A FastAPI app with `POST /api/v1/urls` and `GET /{short_code}` using an in-memory dictionary.

What you should already know: HTTP, FastAPI routing, Python dictionaries.

Components to create:

- `main.py`
- `schemas.py`
- simple in-memory store.

Success looks like: You can create a short code and redirect with `302`.

Do not copy: Existing service/repository files.

## Milestone 2 - Request Validation

What to build: Pydantic schema that validates original URLs and aliases.

What you should already know: Pydantic validators.

Components to create:

- request schema.
- response schema.
- validation tests.

Success looks like: Bad schemes and unsafe localhost URLs are rejected.

Do not copy: Exact validator implementation.

## Milestone 3 - Data Layer

What to build: SQLAlchemy async models and session management.

What you should already know: SQL, ORM models, async sessions.

Components to create:

- database models for URLs and click events.
- session dependency.
- repository methods.

Success looks like: Data survives app restart when using PostgreSQL.

Do not copy: Exact column choices until you can justify them.

## Milestone 4 - Service Layer

What to build: A service that coordinates creation, redirect resolution, analytics, and delete behavior.

What you should already know: layered architecture.

Components to create:

- URL service class.
- repository class.
- API routes.

Success looks like: Route handlers are thin and business rules live in the service.

Do not copy: Function names blindly; choose names you understand.

## Milestone 5 - Short Code Generation

What to build: Unique generated short codes.

What you should already know: uniqueness and base conversion.

Components to create:

- ID generator.
- Base62 encoder.
- collision check.

Success looks like: Generated codes are compact and unique in tests.

Do not copy: Bit constants until you understand their capacity.

## Milestone 6 - Analytics

What to build: Click counting and click-event logging.

What you should already know: database writes and redirect flow.

Components to create:

- click counter update.
- click event insert.
- analytics endpoint.

Success looks like: Redirecting twice increases analytics count by two.

Do not copy: The exact analytics shape; decide what product users need.

## Milestone 7 - Redis Cache

What to build: Cache-aside redirect lookup with graceful Redis fallback.

What you should already know: Redis keys and TTLs.

Components to create:

- Redis client module.
- cache lookup in service.
- cache invalidation on delete.

Success looks like: Redirects still work when Redis is down, and hot URLs use cache when Redis is up.

Do not copy: Silent error handling without deciding what should be logged or alerted.

## Milestone 8 - Middleware Reliability

What to build: Rate limiting and idempotency middleware.

What you should already know: FastAPI/Starlette middleware, Redis sorted sets.

Components to create:

- rate limiter.
- idempotency cache.
- tests for both.

Success looks like: Excess requests get `429`, repeated POST with same key replays safely.

Do not copy: Idempotency behavior without adding request fingerprinting.

## Milestone 9 - Testing

What to build: Unit and integration test suite.

What you should already know: pytest fixtures and HTTPX ASGI transport.

Components to create:

- test database fixture.
- dependency overrides.
- feature tests.

Success looks like: Tests cover create, alias conflict, redirect, analytics, delete, validation, and ID generation.

Do not copy: Tests verbatim; write them from behavior.

## Milestone 10 - Production Hardening

What to build: Auth, migrations, observability, Docker, and deployment.

What you should already know: JWT, Alembic, structured logs, metrics, containers.

Components to create:

- auth endpoints.
- ownership checks.
- migrations.
- structured logging.
- metrics.
- Dockerfile.
- CI workflow.

Success looks like: The app can be deployed, upgraded, monitored, and debugged.

Do not copy: README production claims; implement and verify each claim.

