# Knowledge Prerequisites

## A. Essential Prerequisites

### Python Fundamentals

Difficulty: Beginner.

Why it matters: The entire application is Python.

Where it appears: Every file in `src/` and `tests/`.

Recommended depth: Functions, classes, imports, exceptions, type hints, context managers.

Learn before it: Basic programming.

### HTTP And REST APIs

Difficulty: Beginner to intermediate.

Why it matters: The system is an HTTP API with redirects.

Where it appears: `src/main.py`, `src/api/v1/urls.py`, integration tests.

Recommended depth: Methods, status codes, headers, request bodies, response models, `302` redirects.

Learn before it: Basic web concepts.

### Async Programming

Difficulty: Intermediate.

Why it matters: FastAPI routes, SQLAlchemy sessions, Redis calls, and tests are asynchronous.

Where it appears: `async def` route handlers, `get_db()`, repository methods, tests with `pytest.mark.asyncio`.

Recommended depth: `async`, `await`, event loop basics, async context managers.

Learn before it: Python functions and exception handling.

### Relational Databases

Difficulty: Intermediate.

Why it matters: URL records and click events persist in database tables.

Where it appears: `src/db/models.py`, `src/repositories/url_repository.py`.

Recommended depth: tables, rows, primary keys, indexes, uniqueness, updates, transactions.

Learn before it: Data modeling basics.

### Testing Basics

Difficulty: Beginner to intermediate.

Why it matters: Tests are the fastest way to learn expected behavior.

Where it appears: `tests/`.

Recommended depth: assertions, fixtures, unit tests, integration tests, dependency overrides.

Learn before it: Python functions and modules.

## B. Concepts To Learn While Studying The Project

### FastAPI Dependency Injection

Difficulty: Intermediate.

Why it matters: Routes receive `URLService` without constructing it manually.

Where it appears: `src/api/deps.py`, route handler parameters.

Recommended depth: `Depends`, dependency overrides in tests, lifecycle of per-request dependencies.

Learn before it: HTTP routes and Python callables.

### Pydantic Validation

Difficulty: Intermediate.

Why it matters: Invalid URLs and aliases are rejected before business logic runs.

Where it appears: `src/schemas/url.py`.

Recommended depth: `BaseModel`, `Field`, `field_validator`, response schemas.

Learn before it: Python classes and data types.

### SQLAlchemy Async ORM

Difficulty: Intermediate to advanced.

Why it matters: Database operations are implemented with async sessions and ORM models.

Where it appears: `src/db/session.py`, `src/db/models.py`, `src/repositories/url_repository.py`.

Recommended depth: engine, sessionmaker, declarative models, `select`, `update`, `commit`, `refresh`.

Learn before it: SQL and async basics.

### Redis Cache-Aside

Difficulty: Intermediate.

Why it matters: Redirects first check Redis before falling back to the database.

Where it appears: `src/core/redis.py`, `src/services/url_service.py`.

Recommended depth: keys, TTL, cache miss, cache invalidation, fallback behavior.

Learn before it: HTTP, databases, key-value stores.

### ID Generation And Base62

Difficulty: Intermediate.

Why it matters: Auto-generated short codes come from Snowflake IDs encoded as compact strings.

Where it appears: `src/services/snowflake.py`, `src/services/base62.py`.

Recommended depth: uniqueness, monotonic IDs, bit shifts, base conversion.

Learn before it: integers, modulo arithmetic, binary basics.

## C. Advanced Concepts

### Distributed Rate Limiting

Difficulty: Advanced.

Why it matters: Middleware uses Redis sorted sets to apply a sliding-window rate limit.

Where it appears: `src/api/middleware.py`.

Recommended depth: sliding window log, atomic pipelines, multi-process consistency, memory cost.

Learn before it: Redis and HTTP middleware.

### Idempotency

Difficulty: Advanced.

Why it matters: Retried POST requests can return the same cached response.

Where it appears: `src/api/middleware.py`.

Recommended depth: idempotency keys, replay safety, response caching, expiration.

Learn before it: HTTP methods and Redis.

### Circuit Breaker Pattern

Difficulty: Advanced.

Why it matters: Implemented as a standalone service utility and tested, but not wired into main flows.

Where it appears: `src/services/circuit_breaker.py`, `tests/unit/test_circuit_breaker.py`.

Recommended depth: closed, open, half-open states; fail-fast; recovery.

Learn before it: async calls and error handling.

### Production Observability

Difficulty: Advanced.

Why it matters: Logs exist, but metrics and tracing are missing. A production system needs all three.

Where it appears: `src/core/logging.py` and roadmap production exercises.

Recommended depth: structured logs, metrics, traces, correlation IDs, dashboards.

Learn before it: HTTP request lifecycle and failure modes.

