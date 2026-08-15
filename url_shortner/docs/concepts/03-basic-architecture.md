# Concept 03 — Single-Service Monolith Baseline Architecture

# 1. Why Start Simple?
Over-engineering a new application with microservices, Kafka, Redis clusters, and sharding introduces debugging friction, deployment complexity, and network overhead.

Start with the simplest working system first:

```text
               [ Client ]
                   │
                   ▼
            [ Load Balancer ]
                   │
                   ▼
            [ API Server ]
            /            \
           ▼              ▼
     [ PostgreSQL ]    [ Redis ]
```

---

# 2. Layered Clean Architecture

To keep monolithic code maintainable, we isolate responsibilities:

1. **API Layer (`src/api/`)**: Handles HTTP parsing, FastAPI routers, and Pydantic validation.
2. **Service Layer (`src/services/`)**: Implements business rules (Base62 encoder, expiration checks).
3. **Repository Layer (`src/repositories/`)**: Encapsulates SQL database access methods.
4. **Database Layer (`src/db/`)**: Manages async database connections and sessions.
