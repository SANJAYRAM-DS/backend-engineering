# Hands-On Exercises

## Beginner Exercises

### 1. Run The Test Suite

Task: Run unit and integration tests.

Files: `tests/`, `requirements.txt`.

Goal: Learn expected behavior before changing code.

Success: You can explain what each integration test proves.

### 2. Change The Short URL Base

Task: Change `BASE_URL` in `.env` or test settings and create a short URL.

Files: `src/core/config.py`, `.env.example`, `src/services/url_service.py`.

Goal: Understand configuration-driven responses.

Success: `short_url` uses the configured base URL.

### 3. Add A Reserved Alias Rule

Task: Reject aliases such as `api`, `docs`, and `openapi.json`.

Files: `src/schemas/url.py`, `tests/unit/test_url_validation.py`.

Goal: Practice validation.

Success: Tests prove reserved aliases are rejected.

### 4. Add A Metadata Endpoint

Task: Add `GET /api/v1/urls/{short_code}`.

Files: `src/api/v1/urls.py`, `src/services/url_service.py`, `tests/integration/test_url_api.py`.

Goal: Practice route -> service -> repository flow.

Success: Endpoint returns URL metadata without redirecting.

## Intermediate Exercises

### 5. Implement Expiration Tests

Task: Test that expired URLs return `404` on redirect.

Files: `tests/integration/test_url_api.py`, `src/services/url_service.py`.

Goal: Understand time-sensitive behavior.

Success: Expired short codes cannot redirect.

### 6. Add `last_accessed_at`

Task: Track the most recent successful redirect time.

Files: `src/db/models.py`, `src/repositories/url_repository.py`, `src/services/url_service.py`.

Goal: Modify database shape and update flow.

Success: Analytics shows the last access time after redirects.

### 7. Make Rate Limits Configurable

Task: Move `window_seconds` and `max_requests` into settings.

Files: `src/core/config.py`, `src/api/middleware.py`.

Goal: Learn production configuration.

Success: Tests can lower the limit and trigger `429`.

### 8. Improve Idempotency Safety

Task: Include request path and request body hash in idempotency storage.

Files: `src/api/middleware.py`.

Goal: Prevent replaying one POST response for a different POST body.

Success: Same key with same body replays; same key with different body returns an error or uses a different storage key.

### 9. Add Auth

Task: Implement registration, login, JWT issuance, and protected delete/analytics.

Files: `src/db/models.py`, `src/api/v1/`, `src/api/deps.py`, `requirements.txt`.

Goal: Turn the unused `User` model and auth dependencies into real functionality.

Success: Users can only delete or view analytics for their own URLs.

## Advanced Exercises

### 10. Add Alembic Migrations

Task: Replace startup `create_all` with migrations.

Files: `src/db/models.py`, new `alembic/` files.

Goal: Learn production schema evolution.

Success: Schema changes are versioned and applied through migration commands.

### 11. Add Structured Logging And Correlation IDs

Task: Add request IDs and structured log fields.

Files: `src/core/logging.py`, `src/api/middleware.py`.

Goal: Make debugging production requests easier.

Success: Every request log includes method, path, status code, latency, and request ID.

### 12. Add Prometheus Metrics

Task: Track request count, latency, redirects, cache hits, cache misses, and errors.

Files: `src/main.py`, `src/api/middleware.py`, `src/services/url_service.py`.

Goal: Learn operational visibility.

Success: `/metrics` exposes useful metrics.

### 13. Add Async Analytics Queue

Task: Move click telemetry out of the redirect hot path.

Files: `src/services/url_service.py`, new worker or queue module.

Goal: Keep redirects fast under load.

Success: Redirect works even if analytics processing is slow.

### 14. Fix And Harden Docker

Task: Correct Compose indentation and write a real Dockerfile.

Files: `docker-compose.yml`, `Dockerfile`.

Goal: Make the app runnable in containers.

Success: API, PostgreSQL, and Redis start together and tests can be run in a containerized environment.

### 15. Add Load Testing

Task: Use a load-testing tool to measure redirect latency and database pressure.

Files: new `tests/load/` or docs.

Goal: Learn bottleneck discovery.

Success: You can identify whether bottleneck is app CPU, Redis, DB, or connection pool.

