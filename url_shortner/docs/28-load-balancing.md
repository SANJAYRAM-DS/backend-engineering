# 28 — Load Balancing & Stateless Horizontal API Scaling

## 1. Learning Objective
Configure Nginx / HAProxy / Traefik load balancers using Round Robin, Least Connections, and IP Hash algorithms to distribute HTTP traffic across stateless API nodes.

---

## 2. Layer 4 vs Layer 7 Load Balancing

- **L4 Load Balancer (TCP/UDP)**: Routes packets based on IP address and port without inspecting HTTP headers. Ultra-high performance (~1 Million QPS).
- **L7 Load Balancer (HTTP/HTTPS)**: Inspects HTTP headers, path routes (`/api/v1/*` vs `/*`), SSL termination, and rate limits.
