# 02 — Requirements Engineering & Capacity Estimation

# 01. Learning Objective

By the end of this document, I should understand:
- How to separate Functional Requirements (FR) from Non-Functional Requirements (NFR).
- How to perform mathematical back-of-the-envelope capacity estimations for storage, throughput (QPS), bandwidth, and RAM.
- How the Pareto 80/20 principle dictates Redis memory sizing.
- How to set quantitative SLA boundaries for write and read latency.

---

# 02. Prerequisites

Before starting this document, I should understand:
- Basic arithmetic and unit conversions (Bytes, KB, MB, GB, TB, QPS).
- Concepts from [01-problem-understanding.md](file:///e:/backend_engineering/url_shortner/docs/01-problem-understanding.md).

---

# 03. Problem We Are Solving

Designing distributed systems without mathematical sizing leads to under-provisioned databases that crash on launch or millions of dollars wasted on over-provisioned cloud infrastructure. We must calculate exact quantitative resource boundaries before writing code.

---

# 04. Functional Requirements (FR)

1. **URL Shortening**: Convert valid target URL to 7-character Base62 code (`short.ly/aB72x`).
2. **URL Redirection**: Resolve short code to target URL via `HTTP 302 Found`.
3. **Custom Aliases**: Allow optional custom code (e.g., `short.ly/my-sale`) with uniqueness enforcement.
4. **Link Expiration (TTL)**: Optional expiration timestamp (`expires_at`).
5. **Click Analytics**: Track click count, time-series distributions, referrers, and user-agent devices.
6. **User Accounts & Auth**: Authenticate users (JWT) and restrict link management to link owners.

---

# 05. Non-Functional Requirements (NFR)

- **High Availability**: 99.99% uptime (~52 minutes downtime/year).
- **Ultra-Low Redirection Latency**: Read p99 < 10ms.
- **Write Latency**: Write p99 < 100ms.
- **Read-Heavy Traffic Ratio**: 100:1 (Read : Write).
- **High Durability**: 99.999999999% (11 Nines) persistence.

---

# 06. Capacity Estimation Math

### Assumptions
- **Monthly New URLs**: 30 Million
- **Read-to-Write Ratio**: 100 : 1
- **Retention**: 10 Years

### Throughput (QPS)
- **Write QPS**: $\frac{30,000,000}{2.6 \times 10^6 \text{ sec/month}} \approx 11.5 \text{ writes/sec}$ (Peak: 23 writes/sec).
- **Read QPS**: $11.5 \times 100 \approx 1,150 \text{ reads/sec}$ (Peak: 2,300 reads/sec).

### Storage Sizing
- **Row Footprint**: ~700 bytes / record in PostgreSQL.
- **5-Year Storage**: $30\text{M} \times 12 \times 5 \times 700\text{ bytes} \approx 1.26 \text{ TB}$.
- **10-Year Storage**: $\approx 2.52 \text{ TB}$.

### RAM Memory Sizing (Pareto 80/20 Rule)
- **Daily Reads**: $1,150 \text{ QPS} \times 86,400 \text{ sec/day} \approx 100 \text{ Million reads/day}$.
- **20% Hot Working Set**: $20 \text{ Million links}$.
- **RAM Required**: $20\text{M} \times 512 \text{ bytes} \approx \mathbf{10.24 \text{ GB RAM}}$ (A 16 GB Redis node handles 100% of hot traffic!).

---

# 30. Interview Questions

1. **How do you calculate Redis memory size for a read-heavy system?**
   - *Answer*: Calculate total daily read requests, apply 80/20 Pareto rule to isolate top 20% hot links, and multiply by entry byte footprint.

---

# 33. Learning Checkpoint

- [ ] I can calculate QPS from monthly traffic volumes.
- [ ] I can size database storage for 5-10 year horizons.
- [ ] I can size Redis RAM using the Pareto 80/20 principle.

---

# 35. What Comes Next

Next document: [docs/03-system-design.md](file:///e:/backend_engineering/url_shortner/docs/03-system-design.md)
