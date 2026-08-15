# 05 — Database Schema Design & PostgreSQL Optimization

# 01. Learning Objective

By the end of this document, I should understand:
- How to design a relational PostgreSQL schema for URLs and Click Events.
- Why proper data types (`BIGSERIAL`, `VARCHAR`, `TIMESTAMPTZ`, `TEXT`) matter for disk & RAM footprint.
- How B-Tree indexes work internally to speed up point lookups from $O(N)$ to $O(\log N)$.
- How to analyze query execution plans using `EXPLAIN ANALYZE`.
- Why database connection pooling (asyncpg) is essential under high concurrency.

---

# 02. Prerequisites

Before starting this document, I should understand:
- Relational database concepts (Primary Keys, Foreign Keys, Indexes) from [02-requirements.md](file:///e:/backend_engineering/url_shortner/docs/02-requirements.md).
- Layered repository pattern from [03-system-design.md](file:///e:/backend_engineering/url_shortner/docs/03-system-design.md).

---

# 03. Problem We Are Solving

Consider a database table with 3 Million short URLs.

Query:
```sql
SELECT original_url FROM urls WHERE short_code = 'aB72x';
```

Without an index on `short_code`, PostgreSQL performs a **Sequential Table Scan**, reading every single disk page into memory. At 3 Million rows, this query takes ~142 ms. Under 2,300 QPS traffic, database CPU hits 100% and crashes the application.

We must optimize database performance so lookups execute in **< 0.1 ms**.

---

# 04. Why This Problem Exists

Disk I/O is 100,000x slower than CPU cache access. Without indexes:
- Sequential scans read gigabytes of table heap data off disk.
- High connection creation overhead causes PostgreSQL worker process memory exhaustion.

---

# 05. Concept / Theory

### Relational Schema Entity-Relationship (ER) Diagram

```text
                       [ users ]
                       +-----------+
                       | id (PK)   |
                       | email     |
                       | password  |
                       +-----+-----+
                             |
                             | 1:N
                             v
                       [ urls ]
                       +------------------+
                       | id (PK)          |
                       | short_code (UQ)  |<---+
                       | original_url     |    |
                       | user_id (FK)     |    | 1:N
                       | created_at       |    |
                       | expires_at       |    |
                       | click_count      |    |
                       | is_active        |    |
                       +------------------+    |
                                               |
                                               v
                                    [ click_events ]
                                    +-----------------+
                                    | id (PK)         |
                                    | short_code (FK) |
                                    | clicked_at      |
                                    | ip_address      |
                                    | user_agent      |
                                    | referrer        |
                                    | country         |
                                    +-----------------+
```

---

# 06. How It Works Internally

### B-Tree Index Execution Mechanics (`EXPLAIN ANALYZE`)

When a UNIQUE B-Tree index is created on `short_code`:

```text
               [ B-Tree Root Node ]
                     /      \
                    /        \
          [ Node "a" - "m" ]  [ Node "n" - "z" ]
                 /
                /
    [ Leaf Node: "aB72x" -> Heap Pointer Page 402 ]
```

#### Query Benchmark Comparison

- **Sequential Scan (No Index)**:
  `Execution Time: 142.350 ms` (Scans 3,000,000 rows).
- **Index Scan (UNIQUE B-Tree Index)**:
  `Execution Time: 0.041 ms` (3,400x performance increase!).

---

# 07. Real-World Usage

High-scale production databases at Stripe, GitHub, and Uber rely heavily on composite B-Tree indexes, partial indexes, and connection pooling to serve tens of thousands of queries per second per database node.

---

# 12. Database Changes (DDL Script)

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: urls
CREATE TABLE IF NOT EXISTS urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(30) NOT NULL,
    original_url TEXT NOT NULL,
    user_id UUID NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NULL,
    click_count BIGINT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT chk_short_code_min_length CHECK (char_length(short_code) >= 3),
    CONSTRAINT chk_original_url_format CHECK (original_url ~* '^https?://')
);

-- Table: click_events
CREATE TABLE IF NOT EXISTS click_events (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(30) NOT NULL,
    clicked_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    referrer TEXT NULL,
    country VARCHAR(3) NULL
);

-- Indexes
CREATE UNIQUE INDEX idx_urls_short_code ON urls(short_code);
CREATE INDEX idx_urls_user_id ON urls(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_click_events_code_time ON click_events(short_code, clicked_at DESC);
```

---

# 14. Folder/File Changes

- `src/db/session.py` — Database engine & connection pool
- `src/db/models.py` — SQLAlchemy ORM models (`URL`, `ClickEvent`)
- `src/repositories/url_repository.py` — Async database access layer

---

# 16. Complete Code

### SQLAlchemy ORM Models (`src/db/models.py`)
```python
import datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Index,
    String,
    Text,
)
from sqlalchemy.sql import func
from src.db.session import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    short_code = Column(String(30), unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    user_id = Column(String(36), nullable=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at = Column(DateTime(timezone=True), nullable=True)
    click_count = Column(BigInteger, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        Index("idx_urls_short_code_active", "short_code", "is_active"),
    )


class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    short_code = Column(String(30), nullable=False, index=True)
    clicked_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    referrer = Column(Text, nullable=True)
    country = Column(String(3), nullable=True)

    __table_args__ = (
        Index("idx_click_events_code_time", "short_code", "clicked_at"),
    )
```

---

# 30. Interview Questions

1. **What is the time complexity of a B-Tree index lookup versus a Sequential Table Scan?**
   - *Answer*: B-Tree index lookup is $O(\log N)$; Sequential Scan is $O(N)$.
2. **Why is connection pooling critical for async database drivers like `asyncpg`?**
   - *Answer*: Opening raw PostgreSQL connections incurs TCP and TLS handshakes and forks database processes. Connection pooling reuses pre-established connections, preventing RAM exhaustion.

---

# 33. Learning Checkpoint

- [ ] I can write PostgreSQL DDL schemas.
- [ ] I understand how B-Tree indexes accelerate queries.
- [ ] I can analyze query performance with `EXPLAIN ANALYZE`.

---

# 35. What Comes Next

Next document: [docs/06-project-setup.md](file:///e:/backend_engineering/url_shortner/docs/06-project-setup.md)
