# 42 — Exponential Backoff & Jitter

## 1. Learning Objective
Deep dive into network backoff math, preventing Thundering Herd problems during cluster recovery.

---

## 2. Thundering Herd Problem

When a database node restarts, 1,000 waiting API instances simultaneously retry calls. Without randomized jitter, all 1,000 instances hit the database at the exact same millisecond, crashing it again.

Adding randomized Jitter spreads retry attempts evenly across time.
