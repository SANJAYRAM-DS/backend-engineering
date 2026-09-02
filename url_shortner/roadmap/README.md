# Master Learning Roadmap

This roadmap is based on the actual code in this repository, not only the README. The project is a FastAPI URL shortener with async SQLAlchemy persistence, optional Redis caching, Snowflake-style ID generation, Base62 short codes, request validation, rate limiting, idempotency support, click analytics, and pytest coverage.

The README describes a larger production-grade distributed system. The current implementation is a strong learning baseline for that architecture, but several production claims are aspirational or partially implemented. The roadmap separates implemented behavior from future production work.

## Files In This Roadmap

1. [01-codebase-analysis.md](01-codebase-analysis.md) - what the project does, structure, high-value files, startup behavior.
2. [02-architecture.md](02-architecture.md) - reconstructed architecture, responsibilities, dependencies, data flow.
3. [03-knowledge-prerequisites.md](03-knowledge-prerequisites.md) - prerequisites, project-time concepts, advanced topics.
4. [04-technology-stack.md](04-technology-stack.md) - core, supporting, optional, and aspirational technologies.
5. [05-concept-dependency-graph.md](05-concept-dependency-graph.md) - what to learn first and why.
6. [06-learning-roadmap.md](06-learning-roadmap.md) - phase-by-phase learning path.
7. [07-concepts-connected-to-code.md](07-concepts-connected-to-code.md) - major concepts mapped to real files.
8. [08-file-by-file-learning-order.md](08-file-by-file-learning-order.md) - efficient inspection order and "do not read yet" list.
9. [09-execution-flows.md](09-execution-flows.md) - create, redirect, analytics, delete, startup, rate limiting, idempotency.
10. [10-patterns-and-production-engineering.md](10-patterns-and-production-engineering.md) - patterns, production concerns, gaps.
11. [11-hands-on-exercises.md](11-hands-on-exercises.md) - beginner, intermediate, and advanced exercises.
12. [12-rebuild-from-scratch.md](12-rebuild-from-scratch.md) - rebuild milestones without copying source.
13. [13-why-built-this-way.md](13-why-built-this-way.md) - architectural decisions and trade-offs.
14. [14-interview-and-mastery-test.md](14-interview-and-mastery-test.md) - interview questions, answer guidelines, final practical test.
15. [15-80-20-priority-map.md](15-80-20-priority-map.md) - must learn, should learn, nice to know, advanced.

## Master Phase Map

```text
PHASE 0
Prerequisites
    |
PHASE 1
Core Technologies
    |
PHASE 2
Architecture
    |
PHASE 3
Codebase
    |
PHASE 4
Core Features
    |
PHASE 5
Advanced Concepts
    |
PHASE 6
Testing + Debugging
    |
PHASE 7
Production Engineering
    |
PHASE 8
Rebuild From Scratch
    |
PHASE 9
Independent Project
```

## The 80/20 Summary

If you only study five things first, study these:

1. FastAPI request lifecycle: `src/main.py`, `src/api/v1/urls.py`, `src/api/deps.py`.
2. Service and repository split: `src/services/url_service.py`, `src/repositories/url_repository.py`.
3. Database modeling and async sessions: `src/db/models.py`, `src/db/session.py`.
4. Short code generation: `src/services/snowflake.py`, `src/services/base62.py`.
5. Reliability around hot paths: `src/core/redis.py`, `src/api/middleware.py`, `tests/`.

