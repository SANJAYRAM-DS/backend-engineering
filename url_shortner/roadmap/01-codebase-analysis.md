# Codebase Analysis

## What Problem This Project Solves

This project turns long destination URLs into short codes and redirects users from short links to the original destination. It also tracks basic analytics through a click counter and click-event table.

Primary users:

- Developers learning backend engineering and system design.
- Product teams needing a small URL shortener API.
- Students studying FastAPI, async database access, Redis caching, validation, and service layering.

## Major Features Actually Implemented

- Create short URLs with generated short codes.
- Create short URLs with custom aliases.
- Redirect from `/{short_code}` to the original URL.
- Fetch basic analytics for a short code.
- Soft-delete a short URL by marking it inactive.
- Validate original URLs and custom aliases.
- Block obvious localhost, loopback, private IP, reserved IP, and link-local targets.
- Generate unique IDs with a Snowflake-style generator.
- Encode numeric IDs into Base62 strings.
- Use Redis as an optional cache.
- Fall back when Redis is unavailable.
- Rate-limit requests by client IP.
- Cache successful POST responses when an `Idempotency-Key` header is used.
- Test core behavior with pytest, pytest-asyncio, HTTPX, and in-memory SQLite.

## Features Described But Not Fully Implemented

- Authentication and authorization: a `User` model exists, but there are no auth endpoints or JWT flows.
- Kafka analytics: mentioned in documentation, not present in code.
- Prometheus, OpenTelemetry, and distributed tracing: mentioned, not implemented.
- Docker production image: `Dockerfile` is only a placeholder.
- Migrations: Alembic is mentioned in docs but not configured in the repo.
- Multi-region, sharding, replication, CDN, NGINX, and advanced load balancing: useful system-design topics, not implemented locally.

## Directory Structure

```text
url_shortner/
|-- src/
|   |-- main.py
|   |-- api/
|   |   |-- deps.py
|   |   |-- middleware.py
|   |   `-- v1/urls.py
|   |-- core/
|   |   |-- config.py
|   |   |-- logging.py
|   |   `-- redis.py
|   |-- db/
|   |   |-- models.py
|   |   `-- session.py
|   |-- repositories/
|   |   `-- url_repository.py
|   |-- schemas/
|   |   `-- url.py
|   `-- services/
|       |-- base62.py
|       |-- circuit_breaker.py
|       |-- snowflake.py
|       `-- url_service.py
|-- tests/
|   |-- conftest.py
|   |-- integration/test_url_api.py
|   `-- unit/
|-- docs/
|-- roadmap/
|-- requirements.txt
|-- docker-compose.yml
|-- Dockerfile
`-- .env.example
```

## High-Value Files

### `src/main.py`

Entry point for the FastAPI app. It configures lifespan startup/shutdown, creates database tables, registers middleware, mounts the API router, and defines the redirect endpoint.

### `src/api/v1/urls.py`

Defines the API contract for creating URLs, reading analytics, and deleting URLs. It is intentionally thin and delegates business logic to `URLService`.

### `src/services/url_service.py`

The core application logic. It decides how short codes are generated, checks alias conflicts, writes to the repository, talks to Redis, resolves redirects, records telemetry, and handles cache invalidation.

### `src/repositories/url_repository.py`

The database access layer. It contains SQLAlchemy queries and write operations for URLs and click events.

### `src/db/models.py`

Defines database tables: `User`, `URL`, and `ClickEvent`. The `URL` and `ClickEvent` models are central to current behavior.

### `src/schemas/url.py`

Defines Pydantic request and response schemas. This is where URL validation and custom-alias validation live.

### `src/api/middleware.py`

Implements rate limiting and idempotency behavior. It uses Redis when available and a process-local dictionary as fallback for rate limiting.

### `tests/`

Shows how the system is expected to behave. Tests use dependency overrides to replace PostgreSQL with in-memory SQLite and disable Redis.

## What Happens When The Application Starts

1. Python imports `src.main:app`.
2. Settings are loaded from environment variables and `.env` through `src/core/config.py`.
3. The global async SQLAlchemy engine is configured in `src/db/session.py`.
4. FastAPI creates the app with a lifespan context.
5. On startup, `setup_logging()` runs.
6. Startup attempts `Base.metadata.create_all`, creating tables if the configured database is available.
7. Middleware is registered.
8. API routes are mounted under `/api/v1`.
9. The root-level redirect route `/{short_code}` is available.
10. On shutdown, the database engine is disposed and Redis is closed.

## Main Operations

### Create Short URL

`POST /api/v1/urls` -> `create_short_url()` route -> `URLService.create_short_url()` -> `URLRepository.create_url()` -> optional Redis cache pre-warm -> `URLResponse`.

### Redirect

`GET /{short_code}` -> `redirect_to_url()` -> `URLService.resolve_url()` -> Redis lookup -> database fallback -> click count increment -> click event insert -> `RedirectResponse`.

### Analytics

`GET /api/v1/urls/{short_code}/analytics` -> `URLService.get_analytics()` -> repository lookup -> `AnalyticsResponse`.

### Delete

`DELETE /api/v1/urls/{short_code}` -> `URLService.delete_url()` -> repository soft delete -> Redis key deletion -> `204 No Content`.

