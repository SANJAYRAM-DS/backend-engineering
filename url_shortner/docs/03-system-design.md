# 03 — High-Level System Architecture & System Design

## 1. Learning Objective
In this module, you will learn how to design the high-level architecture of a URL Shortener from an initial simple single-node service to a scalable, modular monolith architecture before introducing distributed components.

---

## 2. Problem
When building a new system, starting with microservices, Kafka, Redis clusters, and database sharding introduces massive operational complexity, debugging overhead, and deployment friction. We need a clean, layered monolithic architecture that allows fast iteration, clear separation of concerns, and easy future decomposition into distributed services.

---

## 3. Theory & Architectural Pattern

### The Layered Software Architecture Pattern (Clean Architecture)
Our application separates responsibilities into four isolated layers:

```text
[ Client (Browser / Mobile / Curl) ]
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                     1. API LAYER                        │
│   (FastAPI Routers, Dependency Injection, Validation)   │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   2. SERVICE LAYER                      │
│ (Business Rules, Base62 Encoder, Security Validation)   │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 3. REPOSITORY LAYER                     │
│    (Database Abstraction, CRUD Data Access Methods)     │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 4. DATABASE LAYER                       │
│    (PostgreSQL Engine, Connection Pool, SQLAlchemy)     │
└─────────────────────────────────────────────────────────┘
```

1. **API Layer (`src/api/`)**: Translates HTTP requests into standard DTOs (Pydantic), invokes service methods, and serializes responses.
2. **Service Layer (`src/services/`)**: Contains pure business logic. It does not know about HTTP requests or raw SQL.
3. **Repository Layer (`src/repositories/`)**: Handles database persistence. Provides a clean Python interface for database queries.
4. **Database Layer (`src/db/`)**: Manages database connections, transactions, and ORM mapping.

---

## 4. Why This Architecture?
- **Testability**: Services can be unit tested without requiring a live database or running web server.
- **Maintainability**: Changing database libraries (e.g., from SQLAlchemy to raw asyncpg) only modifies the Repository layer.
- **Scalability**: Stateless API nodes can be horizontally scaled behind a load balancer.

---

## 5. System Design Diagram: Monolith Phase

```text
+-------------------------------------------------------------------------+
|                              CLIENT LAYER                               |
|                     (Web Browser / Mobile App / CLI)                    |
+-------------------------------------------------------------------------+
                                     │
                                     │ HTTP (JSON / Redirection)
                                     v
+-------------------------------------------------------------------------+
|                        FASTAPI API CONTAINER                            |
|                                                                         |
|  POST /api/v1/urls  ──> [ URL Router ] ──> [ URL Service ] ──┐          |
|  GET /{short_code}  ──> [ Redirect Router ] ───────────────────┼──┐     |
|                                                                │  │     |
|  [ Repository Layer ] <────────────────────────────────────────┘  │     |
|          │                                                        │     |
|          └──────> [ PostgreSQL Connection Pool (asyncpg) ]        │     |
|                                  │                                │     |
+----------------------------------|--------------------------------|-----+
                                   │                                │
                                   v                                v
+------------------------------------+    +-------------------------------+
|         POSTGRESQL DATABASE        |    |          REDIS CACHE          |
|  (Primary Data & Index Storage)    |    |  (Added in Caching Module)    |
+------------------------------------+    +-------------------------------+
```

---

## 6. Files Involved in Phase 1 & 2 Setup

- [src/main.py](file:///e:/backend_engineering/url_shortner/src/main.py) — Application entry point
- [src/core/config.py](file:///e:/backend_engineering/url_shortner/src/core/config.py) — Application configuration
- [src/core/logging.py](file:///e:/backend_engineering/url_shortner/src/core/logging.py) — Structured logging
- [src/db/session.py](file:///e:/backend_engineering/url_shortner/src/db/session.py) — Database session management

---

## 7. Trade-offs Analysis

| Architecture Option | Advantages | Disadvantages | Decision |
| :--- | :--- | :--- | :--- |
| **Microservices from Day 1** | Independent service deployment | Complex network IPC, distributed tracing needed, hard local debugging | Rejected |
| **Layered Monolith** | Single repository, simple deployment, fast local testing, clear boundaries | Single codebase scaled together | **Selected for Phase 1-3** |

---

## 8. Learning Checkpoint & Questions

1. Why should API routers never contain direct raw SQL queries?
2. What is the role of the Repository pattern in modern software architecture?
3. How does statelessness in the API layer facilitate horizontal scaling?
