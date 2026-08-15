# 56 — Infrastructure Cost Analysis & Sizing

## 1. Learning Objective
Calculate total monthly cloud infrastructure hosting costs (AWS / GCP / Bare Metal) for Small, Medium, and Large scale URL shortener deployments.

---

## 2. Deployment Tiers & Monthly Cost Estimation

### Tier 1: Startup Scale (1 Million Reads/Month)
- 1x API Node (t3.micro): $8 / mo
- 1x Managed PostgreSQL (db.t3.micro): $15 / mo
- **Total Cost**: **~$23 / month**

### Tier 2: Mid-Market Scale (100 Million Reads/Month)
- 2x API Nodes (t3.medium): $60 / mo
- 1x Primary + 1x Replica PostgreSQL (db.r6g.large): $350 / mo
- 1x Redis Node (cache.m6g.large): $120 / mo
- 1x Application Load Balancer: $25 / mo
- **Total Cost**: **~$555 / month**

### Tier 3: Global Scale (10 Billion Reads/Month)
- Cloudflare Enterprise CDN/WAF: $3,000 / mo
- 10x API Container Nodes: $1,200 / mo
- Redis Cluster (3 Shards, 6 Nodes): $1,500 / mo
- PostgreSQL Primary + 3 Replicas: $2,800 / mo
- MSK Apache Kafka Cluster: $1,200 / mo
- ClickHouse Analytics Cluster: $2,000 / mo
- **Total Cost**: **~$11,700 / month**
