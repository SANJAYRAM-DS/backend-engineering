# Why Was It Built This Way?

## Decision: FastAPI For The API Layer

Why the author likely chose it: FastAPI is concise, async-friendly, and gives OpenAPI docs automatically.

Problem it solves: Quickly building validated HTTP APIs.

Alternative: Flask, Django REST Framework, Litestar, Express, Go.

Advantages: Good developer experience, async support, Pydantic integration.

Disadvantages: Requires understanding async behavior and dependency injection.

When I would use it: Python API services where speed of development and type-driven validation matter.

## Decision: Service Layer Between Routes And Database

Why the author likely chose it: The app has workflows that span validation, ID generation, caching, and persistence.

Problem it solves: Prevents route handlers from becoming large and hard to test.

Alternative: Put all logic in routes.

Advantages: Better organization, easier unit testing, cleaner feature growth.

Disadvantages: More files and more mental hops.

When I would use it: Any backend where operations are more than basic CRUD.

## Decision: Repository Layer For Database Access

Why the author likely chose it: SQLAlchemy details can be isolated behind methods.

Problem it solves: Keeps business logic from directly depending on query construction.

Alternative: Direct ORM calls in services.

Advantages: Easier to change query logic and test persistence behavior.

Disadvantages: Can become a thin pass-through if not used thoughtfully.

When I would use it: Services with repeated queries or clear persistence boundaries.

## Decision: Snowflake IDs Plus Base62

Why the author likely chose it: URL shorteners need compact unique codes without database-counter bottlenecks.

Problem it solves: High-throughput ID generation.

Alternative: UUIDs, random strings, database sequences, hash of original URL.

Advantages: Time-ordered, compact after encoding, scalable across workers if worker IDs are managed.

Disadvantages: Requires clock correctness and worker ID coordination.

When I would use it: Distributed systems needing sortable unique IDs.

## Decision: Redis Cache-Aside For Redirects

Why the author likely chose it: URL shorteners are heavily read-biased.

Problem it solves: Avoids hitting PostgreSQL for every redirect.

Alternative: Always query DB, write-through cache, local memory cache.

Advantages: Lower latency for hot short codes and less database pressure.

Disadvantages: Cache invalidation and stale data become concerns.

When I would use it: Read-heavy lookup paths where slightly stale data can be managed.

## Decision: Soft Delete

Why the author likely chose it: Deleted short codes may need auditability and should not simply disappear.

Problem it solves: Preserves historical data and avoids destructive deletes.

Alternative: Hard delete rows.

Advantages: Safer, easier recovery, analytics can remain possible.

Disadvantages: Every query must filter inactive rows correctly.

When I would use it: User-facing records where deletion history matters.

## Decision: Middleware For Rate Limiting And Idempotency

Why the author likely chose it: These behaviors apply across requests and should run before business logic.

Problem it solves: Prevents duplicated code in every endpoint.

Alternative: Decorators or explicit service calls in routes.

Advantages: Centralized enforcement.

Disadvantages: Harder to reason about response body streaming and route-specific exceptions.

When I would use it: Cross-cutting request policies.

## Decision: Graceful Redis Fallback

Why the author likely chose it: The core URL shortener should remain usable when cache is down.

Problem it solves: Avoids total outage for a cache failure.

Alternative: Fail requests when Redis is down.

Advantages: Better availability.

Disadvantages: Higher database load and weaker distributed rate limiting.

When I would use it: Redis is an optimization, not the source of truth.

## Decision: Tests Use SQLite And Dependency Overrides

Why the author likely chose it: Tests run fast without external services.

Problem it solves: Developer feedback loop.

Alternative: Spin up PostgreSQL and Redis for every test run.

Advantages: Fast and isolated.

Disadvantages: SQLite behavior is not identical to PostgreSQL.

When I would use it: Unit/integration tests for app behavior, with separate database-specific tests for production parity.

