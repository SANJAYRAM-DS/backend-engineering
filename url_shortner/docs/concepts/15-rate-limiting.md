# Concept 15 — Rate Limiting Algorithms & Distributed Defense

# 1. Why Rate Limiting?
Protects backend services against API abuse, brute-force short code harvesting, and Denial of Service (DDoS) attacks.

---

# 2. Rate Limiting Algorithms Compared

- **Fixed Window**: Tracks request counts per minute window. Vulnerable to boundary burst spikes at window edges.
- **Sliding Window Log (Redis Sorted Set)**: Stores request timestamps in Redis ZSET. Evicts timestamps older than window ($T - 60s$). **Most accurate distributed rate limiter.**
- **Token Bucket**: Fills tokens at constant rate. Allows controlled bursts.
- **Leaky Bucket**: Processes requests at constant outflow rate. Smooths out traffic spikes.
