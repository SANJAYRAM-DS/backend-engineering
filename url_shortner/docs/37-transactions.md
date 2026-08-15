# 37 — Database Transactions & ACID Isolation Levels

## 1. Learning Objective
Understand ACID properties (Atomicity, Consistency, Isolation, Durability) and PostgreSQL Transaction Isolation Levels (Read Committed, Repeatable Read, Serializable).

---

## 2. Isolation Levels

- **Read Committed (Default)**: Prevents Dirty Reads. Queries see committed data.
- **Repeatable Read**: Prevents Non-Repeatable Reads. Queries see snapshot of data at transaction start.
- **Serializable**: Strictest isolation level. Simulates serial execution; throws serialization failures if concurrent transactions conflict.
