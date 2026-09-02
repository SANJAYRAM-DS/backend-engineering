# File-By-File Learning Order

## Step 1

File: `requirements.txt`

Why: It reveals the real stack: FastAPI, Pydantic, SQLAlchemy async, Redis, pytest, HTTPX, JWT/password libraries.

Understand: What technologies are actually installed versus what README claims.

## Step 2

File: `src/main.py`

Why: It is the application entry point and shows startup, shutdown, middleware, routers, and the redirect endpoint.

Understand: How the app is assembled and where request flow begins.

## Step 3

File: `src/api/v1/urls.py`

Why: It defines the public API for create, analytics, and delete.

Understand: How route handlers stay thin and delegate to the service layer.

## Step 4

File: `src/api/deps.py`

Why: It explains how route functions receive `URLService`.

Understand: FastAPI dependency injection and why tests can override dependencies.

## Step 5

File: `src/schemas/url.py`

Why: It defines the API contract and request validation.

Understand: Which inputs are accepted, which are rejected, and how response payloads are shaped.

## Step 6

File: `src/db/models.py`

Why: It defines persistent data.

Understand: `URL`, `ClickEvent`, and the currently-unused `User` model.

## Step 7

File: `src/db/session.py`

Why: It shows how database sessions are created and yielded.

Understand: async engine, pool settings, session factory, and lifecycle.

## Step 8

File: `src/repositories/url_repository.py`

Why: It contains all database operations for current features.

Understand: reads, creates, click count updates, click event writes, and soft deletes.

## Step 9

File: `src/services/url_service.py`

Why: It is the main business logic.

Understand: short code generation, alias conflict checks, Redis caching, expiration checks, analytics writes, and cache invalidation.

## Step 10

File: `src/services/snowflake.py`

Why: It explains how unique numeric IDs are generated.

Understand: timestamp bits, worker bits, datacenter bits, sequence bits, and clock rollback handling.

## Step 11

File: `src/services/base62.py`

Why: It turns Snowflake IDs into compact short codes.

Understand: base conversion and why the result is URL-safe.

## Step 12

File: `src/core/redis.py`

Why: It shows optional external dependency handling.

Understand: lazy Redis connection, ping check, fallback to `None`, shutdown cleanup.

## Step 13

File: `src/api/middleware.py`

Why: It contains cross-cutting reliability concerns.

Understand: sliding-window rate limiting, in-memory fallback, idempotency response replay.

## Step 14

File: `tests/conftest.py`

Why: It shows how the app is tested without real PostgreSQL or Redis.

Understand: dependency overrides, in-memory SQLite, HTTPX ASGI transport.

## Step 15

File: `tests/integration/test_url_api.py`

Why: It documents expected behavior better than prose.

Understand: create, custom alias, conflict, redirect, analytics, delete, and 404 behavior.

## Step 16

Files: `tests/unit/test_base62.py`, `tests/unit/test_snowflake.py`, `tests/unit/test_url_validation.py`, `tests/unit/test_circuit_breaker.py`

Why: These isolate individual concepts.

Understand: how to test pure functions, validators, ID generators, and resilience utilities.

## Do Not Read Yet

### `docs/`

Reason: Useful for system-design context, but it may describe features not present in the actual source. Read it after you understand the code.

### `src/services/circuit_breaker.py`

Reason: It is implemented and tested, but not wired into the main request flow. Read it after core create/redirect paths.

### `Dockerfile`

Reason: It is currently a placeholder, so it can confuse you if you expect production Docker behavior.

### `docker-compose.yml`

Reason: It is relevant, but inspect after application architecture. Also note that the Redis service appears incorrectly nested under `postgres`, so it likely needs correction before use.

