# Concept Dependency Graph

Learn this repository in dependency order, not alphabetically.

```text
Python Fundamentals
    |
HTTP + REST + Redirects
    |
FastAPI Routing
    |
Pydantic Request/Response Schemas
    |
Async Programming
    |
SQL + Relational Modeling
    |
SQLAlchemy Async Sessions + ORM Models
    |
Repository Pattern
    |
Service Layer
    |
Short Code Generation
    |-- Snowflake IDs
    `-- Base62 Encoding
    |
Redis Basics
    |
Cache-Aside Redirect Flow
    |
Middleware
    |-- Rate Limiting
    `-- Idempotency
    |
Testing Async APIs
    |
Debugging + Error Handling
    |
Production Engineering
    |-- Authentication
    |-- Authorization
    |-- Migrations
    |-- Observability
    |-- Docker Hardening
    |-- Async Analytics
    `-- Scalability Design
```

## Why This Order Works

Start with Python and HTTP because every important file assumes them. Move to FastAPI and Pydantic because those define the public API boundary. Then learn async and SQLAlchemy because database calls shape most real behavior. After that, the service/repository split becomes clear.

Only then study Snowflake and Base62. They are important, but they make more sense once you understand why a URL shortener needs unique compact identifiers.

Redis, rate limiting, and idempotency should come later because they are optimizations and reliability features around the core API. Testing and production engineering come last because they require a mental model of the whole system.

