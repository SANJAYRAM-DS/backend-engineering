# ResourceHub — Architecture Design Specification (Day 2)

## 1. Architectural Evolution Overview

ResourceHub is designed following an evolutionary architecture model. It begins with a clean, low-complexity monolithic baseline for maximum developer velocity and predictable debugging. As traffic concurrency, dataset volume, and operational requirements scale, the architecture smoothly transitions into a horizontally scalable, decoupled system.

---

## 2. Phase 1 — Initial Architecture (Day 2 Baseline)

In Phase 1, the focus is on simplicity, strict domain boundaries, and single-node consistency.

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                           │
│           (Web App / Mobile App / Postman / CLI)             │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / HTTPS (JSON Payload)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Server                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Middleware (Auth JWT, CORS, Request ID, Logging)      │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ Routers / Controllers (Pydantic Validation, Routing) │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ Service Layer (Business Rules & Domain Authorization) │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ Repository Layer (SQLAlchemy ORM Data Access)         │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Async Connection Pool (asyncpg)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                       │
│     (Relational ACID Storage for Users, Projects, Tasks)    │
└─────────────────────────────────────────────────────────────┘
```

### Baseline Request-Response Flow:
1. **Client** issues an HTTP POST request to `/api/v1/projects/101/tasks` with a JSON payload and Bearer JWT token.
2. **FastAPI Middleware** intercepts the request, verifies the JWT signature, and attaches the authenticated `user_id` to `request.state`.
3. **Controller (Router)** validates the JSON body against a Pydantic `TaskCreate` schema.
4. **Service Layer** verifies that the user has the required project permissions (`OWNER`, `ADMIN`, or `MEMBER`).
5. **Repository Layer** executes an async SQL `INSERT` statement via SQLAlchemy and commits the transaction to PostgreSQL.
6. **PostgreSQL** guarantees ACID compliance and persists the task.
7. **Controller** wraps the created record into the standard HTTP response envelope and returns `201 Created`.

---

## 3. Phase 2 — Future Scale Architecture (Target System)

When traffic grows beyond the capacity of a single server node, components are split out horizontally to isolate failures and maintain performance.

```
                           ┌──────────────┐
                           │    Client    │
                           └──────┬───────┘
                                  │ HTTPS
                                  ▼
                       ┌──────────────────────┐
                       │    Load Balancer     │
                       │   (Nginx / HAProxy)  │
                       └──────────┬───────────┘
                                  │ Round-Robin / Least Conn
           ┌──────────────────────┴──────────────────────┐
           ▼                                             ▼
┌─────────────────────┐                       ┌─────────────────────┐
│  FastAPI Instance 1 │                       │  FastAPI Instance 2 │
│ (Stateless Web App) │                       │ (Stateless Web App) │
└──────────┬──────────┘                       └──────────┬──────────┘
           │                                             │
           ├──────────────────────┬──────────────────────┤
           │                      │                      │
           ▼                      ▼                      ▼
┌─────────────────────┐┌─────────────────────┐┌─────────────────────┐
│ PostgreSQL Primary  ││     Redis Cache     ││    Message Queue    │
│  (All Writes + Core)││ (Tokens & Hot Data) ││ (RabbitMQ / Redis)  │
└──────────┬──────────┘└─────────────────────┘└──────────┬──────────┘
           │ Streaming Replication                       │ Task Messages
           ▼                                             ▼
┌─────────────────────┐                       ┌─────────────────────┐
│ PostgreSQL Replica  │                       │ Background Workers  │
│ (Read Query Offload)│                       │ (Celery Task Nodes) │
└─────────────────────┘                       └─────────────────────┘
```

---

## 4. Learnable Concepts & Component Deep-Dive with Practical Examples

### 1. Client Layer
* **Role:** Web browsers, mobile apps, or third-party API clients.
* **Why it matters:** Sends standard HTTP requests and renders responses.
* **Real-World Example:** A React web dashboard sending `GET /api/v1/projects` with header `Authorization: Bearer eyJhbGci...`.

---

### 2. Load Balancer (e.g., Nginx, HAProxy, AWS ALB)
* **Role:** Distributes incoming network traffic evenly across multiple backend API servers.
* **Why & When Necessary:** A single server can crash or run out of CPU/memory when thousands of users connect simultaneously. A load balancer ensures high availability and zero-downtime deployment.
* **Real-World Example (Flash Sale / Traffic Spike):**
  - Suppose **10,000 users** hit the API at the exact same second.
  - A single FastAPI instance can handle ~2,000 requests/sec before latency spikes.
  - The **Load Balancer** uses a *Round-Robin* or *Least Connections* algorithm to route 2,500 requests each to 4 parallel FastAPI instances (`Instance 1`, `Instance 2`, `Instance 3`, `Instance 4`). If `Instance 2` crashes, the load balancer detects a health check failure and automatically redirects traffic to the remaining healthy instances.

---

### 3. API Instances (FastAPI Servers - Horizontal Scaling)
* **Role:** Stateless application servers handling HTTP routing, validation, and business logic.
* **Why & When Necessary:** Making API servers *stateless* (storing no session data in memory on the web server) allows adding 10 or 100 API instances behind the load balancer dynamically as load increases.
* **Real-World Example:**
  - When user user A makes request #1, it lands on `Instance 1`.
  - When user user A makes request #2 a millisecond later, it lands on `Instance 3`. Because auth relies on stateless JWTs validated against a shared Redis/secret key, `Instance 3` validates the request seamlessly without needing to communicate with `Instance 1`.

---

### 4. Middleware Layer
* **Role:** Cross-cutting interceptor that executes before a request reaches controller logic and after response generation.
* **Why & When Necessary:** Keeps controllers clean by handling cross-cutting concerns (authentication validation, CORS, rate-limit headers, distributed tracing IDs).
* **Real-World Example:**
  - **Request Tracing:** The middleware attaches a unique `X-Request-ID: req_98765` to every incoming request. If a database query fails deep down in the repository layer, all log lines share `req_98765`, enabling instant debugging across distributed log aggregators.

---

### 5. Controller (Router / Presentation Layer)
* **Role:** Parses incoming payloads, enforces input schema validation (Pydantic), formats HTTP responses, and handles HTTP status codes.
* **Why & When Necessary:** Prevents malformed or malicious data from reaching business logic. Decouples HTTP protocols from core domain logic.
* **Real-World Example:**
  - If a client submits `POST /tasks` with `"priority": "SUPER_HIGH"` (invalid priority enum), Pydantic catches it at the Controller layer and immediately returns `422 Unprocessable Entity` with exact field error details, without hitting the database.

---

### 6. Service Layer (Business Logic & Authorization)
* **Role:** Contains enterprise rules, multi-entity orchestration, transaction control, and fine-grained authorization.
* **Why & When Necessary:** Reusable business rules isolated from HTTP routers or CLI callers.
* **Real-World Example:**
  - When a user tries to archive a project, the **Service Layer** checks: (1) Is the user the `OWNER` of the project? (2) Are there any uncompleted tasks marked as `URGENT`? If unauthorized, it raises a domain `PermissionDeniedError` translated by controller to `403 Forbidden`.

---

### 7. Repository Layer (Data Access Layer)
* **Role:** Abstracts raw database interaction (SQLAlchemy ORM queries) behind clean interface methods (`get_by_id`, `create`, `list_active`).
* **Why & When Necessary:** Decouples business logic from specific database drivers or ORM syntax. Allows swapping or mocking databases easily during testing.
* **Real-World Example:**
  - `TaskRepository.get_user_tasks(user_id)` abstracts complex SQL `JOIN` queries between `tasks`, `project_members`, and `users`. The service layer simply calls `task_repo.get_user_tasks(...)` without writing SQL.

---

### 8. PostgreSQL Primary & Read Replicas
* **Role:** Relational ACID storage for core persistent entities.
* **Why & When Necessary:** In heavy applications, **90% of traffic is READ operations** (`SELECT`) and **10% is WRITE operations** (`INSERT`, `UPDATE`, `DELETE`).
* **Real-World Example (Read Offloading):**
  - All write operations (e.g., creating a task, updating profile) hit the **PostgreSQL Primary**.
  - The primary continuously streams updates to **PostgreSQL Read Replicas**.
  - Heavy read queries (e.g., loading project analytics or listing 500 tasks) are offloaded to **Read Replicas**, keeping the Primary DB low on CPU so write operations never lock up.

---

### 9. Redis Cache (In-Memory Data Store)
* **Role:** Ultra-fast sub-millisecond RAM key-value store.
* **Why & When Necessary:** Avoids repetitive disk I/O and expensive SQL queries for static or hot data.
* **Real-World Example (Token Blacklist & Hot Caching):**
  - **Rate Limiting:** Tracking how many requests a user has made in the current minute (e.g., max 100 req/min). Reading and incrementing a counter in Redis takes `< 1ms`, compared to `15-30ms` in SQL.
  - **User Session Cache:** Storing user profile details in Redis key `user:usr_123` so auth middleware doesn't execute a database `SELECT * FROM users` on every single API request.

---

### 10. Message Queue (e.g., RabbitMQ, Redis Streams) & Background Workers (Celery)
* **Role:** Asynchronous task queue for offloading heavy, slow, or third-party operations out of the user's HTTP request-response cycle.
* **Why & When Necessary:** An API request should respond in `< 100ms`. Tasks like sending emails, processing file uploads, or updating audit analytics take hundreds of milliseconds or seconds and shouldn't block the HTTP client.
* **Real-World Example (Async Task Execution):**
  - A user creates a project and invites 20 team members.
  - Instead of making the user wait 5 seconds while the API synchronously sends 20 invitation emails:
    1. FastAPI saves project members in PostgreSQL.
    2. FastAPI pushes a message `{"task": "send_invitation_emails", "project_id": 101}` onto the **Message Queue** (takes 2ms).
    3. FastAPI immediately returns `201 Created` to the user in **25ms**.
    4. **Celery Workers** running on separate background servers pick up the task from the queue and send the emails asynchronously in the background.
