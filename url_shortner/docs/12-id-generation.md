# 12 — Unique ID Generation Strategies

## 1. Learning Objective
Compare single-node auto-increment IDs, UUIDv4, UUIDv7, MD5/SHA256 hash truncation, and distributed Snowflake IDs.

---

## 2. Comparison Matrix

| Strategy | Structure | Pros | Cons | Collision Risk |
| :--- | :--- | :--- | :--- | :--- |
| **PostgreSQL `BIGSERIAL`** | 64-bit auto-increment int | Sequential, compact B-Tree index storage | Predictable (security risk), single DB bottleneck | Zero |
| **UUIDv4** | 128-bit random string | Globally unique across nodes | Non-sequential, fragment B-Tree index pages | Virtually Zero |
| **UUIDv7** | 128-bit time-ordered UUID | Globally unique + B-Tree index friendly | Slightly larger storage footprint (16 bytes) | Zero |
| **Hash Truncation (MD5)** | First 7 chars of `MD5(url)` | Deterministic mapping for duplicate long URLs | High collision rate, requires collision resolution retries | High |
| **Twitter Snowflake** | 64-bit (Timestamp + WorkerID + Sequence) | Time-ordered, distributed, zero DB lock | Requires coordination server / worker ID assignment | Zero |
