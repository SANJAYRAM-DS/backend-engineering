# Concept 05 — Database Design, Indexing & Query Optimization

# 1. Relational Schema Design

```sql
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(30) NOT NULL,
    original_url TEXT NOT NULL,
    user_id UUID NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NULL,
    click_count BIGINT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE click_events (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(30) NOT NULL,
    clicked_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    referrer TEXT NULL,
    country VARCHAR(3) NULL
);
```

---

# 2. Why Indexing is Critical

Primary Redirection Query:
```sql
SELECT original_url FROM urls WHERE short_code = 'aB72x';
```

- **Without Index**: PostgreSQL scans all 3 Million rows (Sequential Scan). **Latency: 142 ms.**
- **With UNIQUE Index (`CREATE UNIQUE INDEX idx_urls_code ON urls(short_code)`)**: PostgreSQL traverses B-Tree root node directly to target heap page. **Latency: 0.041 ms (3,400x speedup!).**
