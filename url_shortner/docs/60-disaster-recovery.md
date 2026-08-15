# 60 — Disaster Recovery & Backup Strategies

## 1. Learning Objective
Formulate a Disaster Recovery (DR) plan covering Recovery Point Objective (RPO) and Recovery Time Objective (RTO).

---

## 2. Backup Metrics & Procedures

- **RPO (Data Loss Window)**: Maximum acceptable data loss duration. Target: **< 1 Minute** (via Continuous WAL archiving to AWS S3 using `pgBackRest`).
- **RTO (Downtime Window)**: Maximum acceptable service outage duration. Target: **< 15 Minutes** (via automated primary failover using `Patroni` / AWS RDS Multi-AZ).
