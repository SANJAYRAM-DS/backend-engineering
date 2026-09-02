# Step-By-Step Learning Roadmap

## PHASE 0 - Prerequisites

What to learn:

- Python functions, classes, modules, type hints, exceptions.
- HTTP methods, status codes, headers, JSON, redirects.
- Basic SQL and relational modeling.

Repository areas to study:

- `src/api/v1/urls.py`
- `src/main.py`
- `src/db/models.py`

Exercises:

- Explain what `POST /api/v1/urls` does in one paragraph.
- Explain why redirect uses `302`.
- Sketch the `urls` and `click_events` tables.

Expected outcome: You can read route handlers and database models without feeling lost.

Prerequisites: Basic programming.

Mastery checkpoint: You can explain request, response, route, model, and table.

## PHASE 1 - Core Technologies

What to learn:

- FastAPI routes and dependency injection.
- Pydantic request and response schemas.
- Async SQLAlchemy sessions.

Repository areas to study:

- `src/api/deps.py`
- `src/schemas/url.py`
- `src/db/session.py`
- `src/repositories/url_repository.py`

Exercises:

- Add a new optional response field in `URLResponse`.
- Add validation for custom aliases to reject aliases starting with `api`.
- Write a repository method to fetch inactive URLs.

Expected outcome: You understand how HTTP inputs become validated Python objects and database writes.

Prerequisites: Phase 0.

Mastery checkpoint: You can trace dependency injection from route to database session.

## PHASE 2 - Architecture

What to learn:

- Layered architecture.
- API layer vs service layer vs repository layer.
- Infrastructure modules.

Repository areas to study:

- `src/main.py`
- `src/api/v1/urls.py`
- `src/services/url_service.py`
- `src/repositories/url_repository.py`
- `src/core/config.py`

Exercises:

- Draw the create-short-URL flow.
- Draw the redirect flow.
- Explain which layer should contain a new business rule and why.

Expected outcome: You can describe component responsibilities and boundaries.

Prerequisites: Phase 1.

Mastery checkpoint: You know where to place route code, validation code, business logic, and SQL.

## PHASE 3 - Codebase

What to learn:

- Startup and shutdown.
- Settings and environment variables.
- Database model creation.
- Optional Redis fallback.

Repository areas to study:

- `src/main.py`
- `src/core/config.py`
- `src/core/redis.py`
- `.env.example`
- `docker-compose.yml`

Exercises:

- Change `BASE_URL` and observe how created short URLs change.
- Break Redis intentionally and verify the app still works without cache.
- Identify the bug in `docker-compose.yml` indentation before trying to run it.

Expected outcome: You understand what must be configured to run locally.

Prerequisites: Phase 2.

Mastery checkpoint: You can explain app startup from import to first request.

## PHASE 4 - Core Features

What to learn:

- Short code generation.
- Alias conflict handling.
- Redirect resolution.
- Analytics writes.
- Soft deletion.

Repository areas to study:

- `src/services/snowflake.py`
- `src/services/base62.py`
- `src/services/url_service.py`
- `src/repositories/url_repository.py`
- `tests/integration/test_url_api.py`

Exercises:

- Add a test for expired URLs.
- Add a test that deleting a missing code returns `404`.
- Modify the generated code length and reason about collision risk.

Expected outcome: You can modify user-visible behavior safely.

Prerequisites: Phase 3.

Mastery checkpoint: You can trace create, redirect, analytics, and delete without opening every file.

## PHASE 5 - Advanced Concepts

What to learn:

- Redis cache-aside.
- Sliding-window rate limiting.
- Idempotency keys.
- Circuit breaker pattern.

Repository areas to study:

- `src/core/redis.py`
- `src/api/middleware.py`
- `src/services/circuit_breaker.py`
- `tests/unit/test_circuit_breaker.py`

Exercises:

- Write a test for rate limiting using the in-memory fallback.
- Write a test for POST idempotency with a fake Redis client.
- Wire `CircuitBreaker` around Redis calls and document the trade-off.

Expected outcome: You understand resilience patterns around the API.

Prerequisites: Phase 4.

Mastery checkpoint: You can explain what happens when Redis is down.

## PHASE 6 - Testing + Debugging

What to learn:

- Unit vs integration tests.
- Async fixtures.
- Dependency overrides.
- HTTPX ASGI testing.

Repository areas to study:

- `tests/conftest.py`
- `tests/unit/`
- `tests/integration/test_url_api.py`

Exercises:

- Add tests for URL expiration.
- Add tests for invalid custom aliases.
- Add tests for analytics after redirect failures.

Expected outcome: You can change code and prove behavior still works.

Prerequisites: Phase 5.

Mastery checkpoint: You can add a feature test before implementing a feature.

## PHASE 7 - Production Engineering

What to learn:

- Authentication and authorization.
- Database migrations.
- Structured logging.
- Metrics and tracing.
- Docker hardening.
- Security validation.

Repository areas to study:

- `src/db/models.py`
- `src/core/logging.py`
- `Dockerfile`
- `requirements.txt`
- `src/schemas/url.py`

Exercises:

- Add Alembic migrations.
- Implement user registration/login using existing `User` model.
- Add ownership checks for delete and analytics.
- Add a `/metrics` endpoint.

Expected outcome: You can distinguish a working app from a production-ready service.

Prerequisites: Phase 6.

Mastery checkpoint: You can list implemented, partial, and missing production concerns.

## PHASE 8 - Rebuild From Scratch

What to learn:

- Recreate the system in milestones without copying code.
- Build from routes inward, then add persistence, caching, tests, and production features.

Repository areas to study:

- Use this repository as a behavioral reference, especially tests.

Exercises:

- Rebuild minimal create and redirect endpoints.
- Add database persistence.
- Add generated short codes.
- Add analytics.
- Add Redis cache.
- Add tests.

Expected outcome: You can implement a URL shortener independently.

Prerequisites: Phase 7.

Mastery checkpoint: Your rebuilt app passes equivalent behavior tests.

## PHASE 9 - Independent Project

What to learn:

- Extend the architecture beyond the original.
- Make deliberate trade-offs.

Repository areas to study:

- All high-value files.

Exercises:

- Add user-owned URL dashboards.
- Add abuse detection.
- Add async analytics queue.
- Add observability.
- Deploy a hardened version.

Expected outcome: You can design, build, debug, and explain a production-minded backend system.

Prerequisites: Phase 8.

Mastery checkpoint: You can defend design choices in an interview-level discussion.

