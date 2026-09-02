# Technology Stack

## Core Technologies

### Python

Why used: Main application language.

What to learn: Type hints, async functions, classes, exceptions, modules, testing.

Where it appears: All `src/` and `tests/` files.

### FastAPI

Why used: Defines async REST APIs, validates request bodies through Pydantic, and generates OpenAPI docs.

What to learn: `FastAPI`, `APIRouter`, route decorators, `Depends`, response models, status codes, middleware.

Where it appears: `src/main.py`, `src/api/v1/urls.py`, `src/api/deps.py`, `src/api/middleware.py`.

### Pydantic V2

Why used: Request and response schema validation.

What to learn: `BaseModel`, `Field`, `field_validator`, validation errors, response serialization.

Where it appears: `src/schemas/url.py`, `src/core/config.py`.

### SQLAlchemy Async

Why used: ORM and database access layer.

What to learn: async engine, async session, declarative models, queries, updates, commits.

Where it appears: `src/db/session.py`, `src/db/models.py`, `src/repositories/url_repository.py`.

### PostgreSQL

Why used: Durable relational database for URLs, users, and click events.

What to learn: tables, indexes, unique constraints, transactions, connection pooling.

Where it appears: configured in `.env.example`, `docker-compose.yml`, `src/core/config.py`.

## Supporting Technologies

### Redis

Why used: Optional cache, rate-limit store, idempotency response store.

What to learn: key-value operations, TTL, sorted sets, pipelines, failure fallback.

Where it appears: `src/core/redis.py`, `src/services/url_service.py`, `src/api/middleware.py`.

### pytest And pytest-asyncio

Why used: Unit and async integration testing.

What to learn: fixtures, async tests, assertions, dependency overrides.

Where it appears: `tests/`.

### HTTPX

Why used: Tests call the ASGI app without starting a real server.

What to learn: `AsyncClient`, `ASGITransport`, redirect behavior.

Where it appears: `tests/conftest.py`, `tests/integration/test_url_api.py`.

### Docker Compose

Why used: Intended local orchestration for PostgreSQL and Redis.

What to learn: services, ports, environment variables, volumes, health checks.

Where it appears: `docker-compose.yml`.

## Optional Or Partially Used Technologies

### JWT And Password Hashing Libraries

Why present: `pyjwt` and `passlib[bcrypt]` are in `requirements.txt`, and a `User` model exists.

Current status: Not wired into auth endpoints or middleware.

What to learn later: password hashing, JWT signing, token verification, authorization policies.

Where it appears: `requirements.txt`, `src/db/models.py`.

### Circuit Breaker

Why present: Demonstrates resilience pattern.

Current status: Implemented and tested, but not integrated into Redis or database calls.

What to learn later: when to wrap external calls, fail-fast behavior, recovery.

Where it appears: `src/services/circuit_breaker.py`.

## Aspirational Technologies Mentioned In Docs But Not Implemented

### Apache Kafka

Mentioned for asynchronous analytics, but no producer, consumer, topic, or dependency exists in the code.

### Prometheus And OpenTelemetry

Mentioned for observability, but no metrics endpoint, tracing SDK, instrumentation, or exporter exists.

### Alembic

Mentioned for migrations, but not installed or configured.

### NGINX, CDN, Multi-Region Infrastructure

Useful production architecture topics, but not part of this runnable repository.

