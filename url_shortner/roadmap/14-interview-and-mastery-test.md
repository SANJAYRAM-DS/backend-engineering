# Interview-Level Understanding And Mastery Test

## Fundamentals Questions

Question: What is the difference between a `301` and `302` redirect?

Answer guideline: Explain permanent vs temporary redirect, browser/proxy caching implications, and why this project uses `302`.

Question: Why is URL validation important in a URL shortener?

Answer guideline: Mention malformed input, SSRF risk, loopback/private IP blocking, phishing risk, and current limits.

Question: What does Base62 solve?

Answer guideline: It converts large integers into compact URL-safe strings.

## Code-Level Questions

Question: What happens inside `URLService.create_short_url()`?

Answer guideline: Discuss alias path, generated-code path, collision checks, repository create, Redis pre-warm, response construction.

Question: Why does `URLRepository.get_by_short_code()` accept `include_inactive`?

Answer guideline: Generated/custom alias conflict checks must consider inactive rows so old codes are not reused accidentally.

Question: What does `tests/conftest.py` override and why?

Answer guideline: It replaces production DB dependency with in-memory SQLite and disables Redis to keep tests fast and deterministic.

## Architecture Questions

Question: Why separate routes, services, and repositories?

Answer guideline: Routes handle HTTP, services handle business workflows, repositories handle persistence. This improves testability and maintainability.

Question: Where would you implement user ownership checks?

Answer guideline: Auth identity is injected at API/dependency layer, but ownership rule belongs in service logic and/or repository query filters.

Question: Where would you put a malware scanning integration?

Answer guideline: Probably service layer or background worker during URL creation, with clear timeout/failure policy.

## Debugging Questions

Question: Redirects return `404` for an existing row. Where do you look?

Answer guideline: Check `is_active`, `expires_at`, `get_by_short_code()` filtering, database connection, cache stale data, route path collisions.

Question: Redis is down. What behavior changes?

Answer guideline: Redirects still query DB, cache pre-warm fails gracefully, distributed rate limiting degrades to in-memory per-process limiting, idempotency stops working.

Question: Click count does not increase. What do you inspect?

Answer guideline: `resolve_url()`, `increment_click_count()`, commit behavior, telemetry exception logs, test DB session state.

## Performance Questions

Question: Where is the hot path?

Answer guideline: `GET /{short_code}` redirect path. It should be optimized because reads dominate writes.

Question: What happens if traffic increases 100x?

Answer guideline: Redis helps reads, but DB click writes become a bottleneck. Need async analytics queue, batching, cache hit metrics, connection pool tuning, load balancing.

Question: What is the bottleneck in current analytics?

Answer guideline: Redirect path performs two database writes: click count update and click event insert.

## Security Questions

Question: What security protections exist?

Answer guideline: Pydantic validation, scheme checks, localhost/private IP blocking, rate limiting, soft deletion.

Question: What security protections are missing?

Answer guideline: Authentication, authorization, ownership checks, strict CORS, URL scanning, abuse reporting, stronger SSRF defenses, admin tooling.

Question: Is the idempotency implementation safe?

Answer guideline: Partially. It caches by key only; should include method/path/body fingerprint and user identity.

## System Design Questions

Question: How would you redesign analytics for high scale?

Answer guideline: Remove click writes from redirect path, publish events to Kafka or queue, process asynchronously, aggregate counters, store raw events separately.

Question: How would you handle hot keys?

Answer guideline: Redis cache, local L1 cache, request coalescing, replicated cache entries, CDN/edge redirect where possible.

Question: How would you shard this system?

Answer guideline: Shard by short code hash or generated ID range, keep lookup deterministic, avoid cross-shard redirect queries.

## Final Mastery Test

### Task 1: Explain Architecture From Memory

Deliverable: Draw the request path from client to route, service, repository, database, Redis, and response.

Pass criteria: You can explain responsibilities without reading code.

### Task 2: Trace Main Flows

Deliverable: Trace create, redirect, analytics, and delete line-by-line through the important files.

Pass criteria: You can name the functions involved and explain data changes.

### Task 3: Add A Feature

Deliverable: Add `last_accessed_at` to analytics.

Pass criteria: You update model, repository, service, schema, and tests coherently.

### Task 4: Debug A Failure

Deliverable: Given "Redis is down and duplicate POSTs are creating duplicate URLs", explain why.

Pass criteria: You connect Redis failure to idempotency loss and propose database-backed idempotency or unique request fingerprints.

### Task 5: Write Tests

Deliverable: Add tests for expired URLs and reserved aliases.

Pass criteria: Tests fail before implementation and pass after implementation.

### Task 6: Identify Trade-Offs

Deliverable: Compare Snowflake+Base62 with random code generation.

Pass criteria: You discuss collision risk, predictability, distributed generation, sorting, and coordination.

### Task 7: Optimize A Component

Deliverable: Redesign click analytics to avoid DB writes during redirect.

Pass criteria: You describe event queue, retry behavior, idempotency, aggregation, and eventual consistency.

### Task 8: Production Readiness Review

Deliverable: Create a production checklist for this app.

Pass criteria: You include auth, migrations, secrets, logging, metrics, tracing, Docker, CI/CD, load testing, backups, and security scanning.

