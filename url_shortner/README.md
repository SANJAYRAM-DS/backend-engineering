# 🚀 Production-Grade Distributed URL Shortener & System Design Masterclass

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.2-DC382D.svg)](https://redis.io/)
[![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-3.6-231F20.svg)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An enterprise-grade, ultra-high-throughput, horizontally scalable distributed URL shortener engineered with Python, FastAPI, Async SQLAlchemy, Redis, Apache Kafka, and Docker. Designed as both a production reference architecture and a hands-on **64-module distributed systems masterclass**.

---

## 📌 Executive Summary

Building real-world backend systems requires more than simple CRUD functionality. This project models the evolution of a URL shortening platform from a single-instance monolith capable of handling modest traffic to a distributed, event-driven, multi-region architecture handling **100,000+ Requests Per Second (RPS)** with sub-10ms redirection latencies and 99.999% availability.

### Key Performance Targets & Architectural Guarantees
- **High Read-to-Write Ratio**: Optimized for 100:1 read vs. write access patterns.
- **Ultra-Low Redirection Latency**: P99 redirection under 10ms using Redis multi-tier caching.
- **Collision-Free Short Codes**: Base62 encoding coupled with high-throughput Snowflake distributed ID generation.
- **Asynchronous Analytics**: Event-driven click logging via Apache Kafka to keep redirection hot-paths non-blocking.
- **Resilience & Rate Limiting**: Distributed Sliding Window Rate Limiting, Circuit Breakers, and Graceful Fallbacks.

---

## 🏗️ High-Level System Architecture

```text
                                       ┌────────────────────────────────┐
                                       │     DNS / Global CDN (Cloud)   │
                                       └───────────────┬────────────────┘
                                                       │
                                                       ▼
                                       ┌────────────────────────────────┐
                                       │  NGINX Reverse Proxy / LB      │
                                       └───────────────┬────────────────┘
                                                       │
                                  ┌────────────────────┴────────────────────┐
                                  ▼                                         ▼
                     ┌────────────────────────┐                ┌────────────────────────┐
                     │   FastAPI Gateway      │                │   FastAPI Gateway      │
                     │   (API Worker 1)       │                │   (API Worker 2)       │
                     └───────────┬────────────┘                └───────────┬────────────┘
                                 │                                         │
       ┌─────────────────────────┼─────────────────────────┬───────────────┴─────────┐
       ▼                         ▼                         ▼                         ▼
┌──────────────┐         ┌──────────────┐          ┌──────────────┐         ┌─────────────────┐
│ Redis Cache  │         │  PostgreSQL  │          │ Apache Kafka │         │ Prometheus /    │
│ (Hot Reads)  │         │  (Primary)   │          │ (Analytics)  │         │ OpenTelemetry   │
└──────────────┘         └──────┬───────┘          └──────┬───────┘         └─────────────────┘
                                │                         │
                         ┌──────┴───────┐          ┌──────┴───────┐
                         ▼              ▼          ▼              ▼
                  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
                  │ Postgres   │ │ Postgres   │ │ Kafka      │ │ Analytics  │
                  │ Replica 1  │ │ Replica 2  │ │ Worker 1   │ │ DB (OLAP)  │
                  └────────────┘ └────────────┘ └────────────┘ └────────────┘
```

---

## 🛠️ Technology Stack & Trade-Off Matrix

| Component | Technology | Rationale & Selection Criteria |
| :--- | :--- | :--- |
| **API Framework** | **FastAPI** (Python 3.11+) | Asynchronous ASGI event-loop (`uvloop`), high concurrency, automatic OpenAPI documentation, Pydantic data validation. |
| **Database (OLTP)** | **PostgreSQL 16** | ACID compliance, robust indexing (B-Tree, BRIN), connection pooling via `asyncpg`, read-replica scalability. |
| **Caching Layer** | **Redis 7.2** | Sub-millisecond latency for hot URLs, atomic string and hash operations, key eviction (LRU), distributed locks. |
| **Event Streaming** | **Apache Kafka 3.6** | High-throughput distributed commit log for decouple click telemetry from the HTTP redirect critical path. |
| **Distributed IDs** | **Twitter Snowflake / Base62** | 64-bit time-ordered unique IDs encoded into 7-character Base62 strings (supporting 3.5+ trillion unique URLs). |
| **Containerization** | **Docker & Docker Compose** | Reproducible multi-service deployment orchestrating API workers, PostgreSQL, Redis, and Kafka. |
| **Testing** | **pytest & pytest-asyncio** | Comprehensive unit testing and async HTTP API integration testing suite. |

---

## 📂 Repository Layout

```text
url_shortner/
├── src/                         # Application Source Code
│   ├── api/                     # REST API Route Controllers
│   │   ├── deps.py              # Dependency Injection (DB, Redis, Auth)
│   │   └── v1/
│   │       └── urls.py          # Shortening & Redirection Endpoints
│   ├── core/                    # Core Configurations & Infrastructure
│   │   ├── config.py            # Pydantic Settings & Environment Validation
│   │   └── logging.py           # Structured JSON Logger
│   ├── db/                      # Database Layer
│   │   ├── models.py            # SQLAlchemy ORM Models
│   │   └── session.py           # Async Engine & Session Manager
│   ├── repositories/            # Data Access Object (DAO) Layer
│   │   └── url_repository.py    # Database Queries & Transaction Boundaries
│   ├── schemas/                 # Pydantic Schemas (DTOs)
│   │   └── url.py               # Request/Response Validation Schemas
│   ├── services/                # Core Business Logic
│   │   ├── base62.py            # Base62 Encoder/Decoder
│   │   └── url_service.py      # Shortening Logic & Cache Integration
│   └── main.py                  # FastAPI Application Entrypoint
├── docs/                        # Master Systems & Architecture Documentation
│   ├── 00-roadmap.md            # Master Curriculum Roadmap
│   ├── architecture-evolution.md# 6-Generation Architecture Journey
│   ├── technology-map.md        # Technical Decision Matrix
│   ├── failure-handbook.md      # Distributed Failure Playbooks
│   ├── interview-preparation.md # System Design Interview Guide
│   ├── final-system-design.md   # Final Blueprint Architecture
│   └── concepts/                # 22 Dedicated Deep-Dive Learning Modules
├── tests/                       # Automated Test Suite
│   ├── conftest.py              # Test Fixtures & In-Memory Test DB
│   ├── integration/             # End-to-End API Integration Tests
│   └── unit/                    # Isolated Business Logic Unit Tests
├── .env.example                 # Environment Variable Blueprint
├── Dockerfile                   # Multi-Stage Production Docker Build
├── docker-compose.yml           # Orchestration Spec for Local Dev & Testing
└── requirements.txt             # Python Package Dependencies
```

---

## ⚡ Quick Start Guide

### Prerequisites
Ensure you have the following installed on your host system:
- **Docker Desktop** (v24.0+) & **Docker Compose** (v2.20+)
- **Python** (v3.11+)
- **Git**

---

### Option 1: Running with Docker Compose (Recommended)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SANJAYRAM-DS/backend-engineering.git
   cd backend-engineering/url_shortner
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   ```

3. **Build & Spin Up All Services**:
   ```bash
   docker-compose up --build -d
   ```

4. **Verify Application Status**:
   ```bash
   docker-compose ps
   ```
   Access the interactive API documentation at: **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

### Option 2: Local Virtual Environment Setup

1. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Start PostgreSQL & Redis**:
   ```bash
   docker-compose up postgres redis -d
   ```

4. **Run FastAPI App in Development Mode**:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 📡 REST API Reference

### 1. Create Short URL
- **Endpoint**: `POST /api/v1/urls`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "original_url": "https://www.example.com/very/long/path/document.html",
    "custom_alias": "my-doc",
    "expires_at": "2026-12-31T23:59:59Z"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "short_code": "my-doc",
    "short_url": "http://localhost:8000/my-doc",
    "original_url": "https://www.example.com/very/long/path/document.html",
    "created_at": "2026-08-15T10:55:00Z",
    "expires_at": "2026-12-31T23:59:59Z"
  }
  ```

### 2. Redirect Short URL
- **Endpoint**: `GET /{short_code}`
- **Response**: `302 Found` (Redirects to original destination URL).

### 3. Fetch URL Analytics
- **Endpoint**: `GET /api/v1/urls/{short_code}/analytics`
- **Response** (`200 OK`):
  ```json
  {
    "short_code": "my-doc",
    "total_clicks": 14250,
    "unique_visitors": 9810,
    "last_accessed_at": "2026-08-15T10:52:12Z"
  }
  ```

### 4. Health Check
- **Endpoint**: `GET /health`
- **Response** (`200 OK`):
  ```json
  {
    "status": "healthy",
    "postgres": "connected",
    "redis": "connected"
  }
  ```

---

## 🧪 Testing & Quality Assurance

Run the automated test suite with coverage reporting:

```bash
# Run unit tests
pytest tests/unit -v

# Run integration tests
pytest tests/integration -v

# Run full test suite with coverage
pytest --cov=src --cov-report=term-missing tests/
```

---

## 🧠 Master Curriculum & Concept Library

This repository contains **22 dedicated deep-dive guides** covering core computer science and distributed systems principles:

| Concept Module | Topic | Key Takeaway |
| :--- | :--- | :--- |
| 📘 [01: Problem Understanding](docs/concepts/01-problem-understanding.md) | Proxy Mechanics & Fundamentals | Understanding reverse proxies and HTTP redirection semantics (301 vs 302). |
| 📘 [02: Requirements Engineering](docs/concepts/02-requirements-engineering.md) | System Math & Capacity Planning | Calculating storage, bandwidth, and CPU requirements for 100M daily active users. |
| 📘 [03: Baseline Architecture](docs/concepts/03-basic-architecture.md) | Single-Service Monolith Baseline | Monolithic performance limits and identifying bottlenecks. |
| 📘 [04: REST API Design](docs/concepts/04-api-design.md) | RESTful Specs & OpenAPI | Clean route design, status codes, and Pydantic schema validation. |
| 📘 [05: Database Design](docs/concepts/05-database-design.md) | Indexing & Query Tuning | B-Tree indexing strategies for O(log N) lookup speed on high-write tables. |
| 📘 [06: ID Generation](docs/concepts/06-id-generation.md) | Short Code Generation Strategies | Counter-based vs Hash-based vs Distributed ID generators. |
| 📘 [07: Base62 Encoding](docs/concepts/07-base62-encoding.md) | Number Systems & Bijective Math | Converting 64-bit integers into compact, URL-safe 7-character strings. |
| 📘 [08: In-Memory Caching](docs/concepts/08-caching-redis.md) | Redis Caching Strategies | Cache-Aside, Write-Through, and Cache-Penetration defense strategies. |
| 📘 [09: Hot-Key Mitigation](docs/concepts/09-hot-key-problem.md) | High-Traffic Key Protection | Local memory caching (L1), key replication, and request coalescing. |
| 📘 [10: Read vs Write Scaling](docs/concepts/10-read-vs-write-scaling.md) | Bottleneck Profiling | Asymmetric scaling techniques for high-read read-heavy workloads. |
| 📘 [11: Database Replication](docs/concepts/11-database-replication.md) | Read Replicas & Lag | Primary-Replica topologies, async replication, and handling stale reads. |
| 📘 [12: Database Sharding](docs/concepts/12-database-sharding.md) | Horizontal Partitioning | Sharding by short code hash and managing cross-shard queries. |
| 📘 [13: Load Balancing](docs/concepts/13-load-balancing.md) | L4 vs L7 Traffic Routing | Round-robin, least connections, consistent hashing algorithms at NGINX/Envoy. |
| 📘 [14: Distributed Snowflake](docs/concepts/14-distributed-ids.md) | Twitter Snowflake Architecture | 64-bit time-ordered unique ID generation across worker nodes without locks. |
| 📘 [15: Rate Limiting](docs/concepts/15-rate-limiting.md) | Distributed Defense | Token Bucket and Sliding Window Log implementation via Redis Lua scripts. |
| 📘 [16: Auth & Authorization](docs/concepts/16-authentication-authorization.md) | Security & IDOR Defense | JWT verification, RBAC permissions, and protecting resource ownership. |
| 📘 [17: Asynchronous Analytics](docs/concepts/17-analytics-async.md) | Non-Blocking Telemetry | Decoupling analytics ingestion from short URL redirection performance. |
| 📘 [18: Apache Kafka](docs/concepts/18-event-driven-kafka.md) | Event-Driven Streaming | Kafka topics, partitions, consumer groups, and backpressure management. |
| 📘 [19: Distributed Resilience](docs/concepts/19-failure-handling-idempotency.md) | Idempotency & Retry Patterns | Exponential backoff with jitter, idempotency keys, and circuit breakers. |
| 📘 [20: Observability](docs/concepts/20-observability.md) | Metrics, Logs & Tracing | Prometheus metrics collection, OpenTelemetry trace propagation, structured logging. |
| 📘 [21: Security Engineering](docs/concepts/21-security-engineering.md) | Abuse & Attack Defense | Rate limiting, SQL injection defense, CORS headers, malicious link scanning. |
| 📘 [22: Production Blueprint](docs/concepts/22-production-architecture.md) | Multi-Region Deployment | Full infrastructure design blueprint for global scale deployment. |

---

## 📚 Master System Documents

- 🗺️ **[00-roadmap.md](docs/00-roadmap.md)** — Master Curriculum Architecture & Learning Dependency Graph
- 📈 **[architecture-evolution.md](docs/architecture-evolution.md)** — Complete 6-Generation Architectural Progression
- 🗺️ **[technology-map.md](docs/technology-map.md)** — Problem-to-Technology Decision & Trade-Off Matrix
- 🛡️ **[failure-handbook.md](docs/failure-handbook.md)** — Centralized Distributed Failure Playbooks
- 🎯 **[interview-preparation.md](docs/interview-preparation.md)** — Master System Design Interview Question Bank
- 🏛️ **[final-system-design.md](docs/final-system-design.md)** — Comprehensive Production System Design Document

---

## 🛡️ Production Readiness & Operational Excellence

- [x] **Strict Type Safety**: Full static type checking via Pydantic v2 schemas and Python type hints.
- [x] **Connection Pooling**: Managed connection pools for both PostgreSQL (`asyncpg`) and Redis (`redis-py`).
- [x] **Graceful Shutdown**: SIGTERM handling to finish in-flight requests and drain connection pools safely.
- [x] **Zero-Downtime Migration**: Database schema versioning ready via Alembic.
- [x] **Security Hardening**: Input sanitization, CORS policy controls, non-root user execution in Docker container.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
