# Concept 02 — Requirements Engineering & System Capacity Sizing

# 1. Functional vs Non-Functional Requirements

### Functional Requirements (FR)
- Shorten target long URLs into 7-character short codes (`short.ly/aB72x`).
- Redirect short URLs via `HTTP 302 Found`.
- Support custom text aliases (e.g., `short.ly/summer-deal`).
- Support optional link expiration dates (`expires_at`).
- Track click telemetry (click counts, referrers, geographic location, user-agents).
- Authenticated user management & link ownership controls.

### Non-Functional Requirements (NFR)
- **Scalability**: Support scaling from 1,000 users up to 10 Billion URLs.
- **Availability**: 99.99% uptime (~52 mins downtime/year). If DB goes down, cached redirects must continue working.
- **Latency**: Ultra-fast redirection (Read p99 < 10ms).
- **Durability**: 99.999999999% (11 Nines) data retention. Created short links must never break due to disk loss.

---

# 2. Back-of-the-Envelope Capacity Estimations

```text
               100:1 Read-to-Write Ratio
 ┌───────────────────────────────────────────────────┐
 │  Writes: 30 Million URLs / month  (~11.5 QPS)     │
 │  Reads:  3 Billion Clicks / month (~1,150 QPS)    │
 └───────────────────────────────────────────────────┘
```

### Storage Calculation (10 Years)
- **Row Footprint**: ~700 bytes per PostgreSQL row.
- **Monthly Storage**: $30\text{M} \times 700\text{ bytes} \approx 21 \text{ GB / month}$.
- **10-Year Database Storage**: $21 \text{ GB} \times 12 \times 10 = \mathbf{2.52 \text{ Terabytes (TB)}}$.

### RAM Memory Calculation (Pareto 80/20 Rule)
- **Daily Reads**: $1,150 \text{ QPS} \times 86,400 \text{ sec/day} = 100 \text{ Million reads/day}$.
- **20% Hot Working Set**: $20 \text{ Million hot links}$.
- **Cache RAM Required**: $20\text{M} \times 512 \text{ bytes} \approx \mathbf{10.24 \text{ GB RAM}}$.
