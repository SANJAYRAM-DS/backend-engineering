# Master Document: System Design Interview Preparation Bank

# 01. Learning Objective

By the end of this document, I should be able to confidently answer beginner, intermediate, advanced, and senior principal system design interview questions about URL shortener architectures.

---

# 02. Comprehensive System Design Question Bank

### Question 1 (Beginner): "Why do we use HTTP 302 Found instead of HTTP 301 Moved Permanently for URL shorteners?"
**Model Answer**: 
> "HTTP 301 Moved Permanently instructs the browser to aggressively cache the redirection locally in its browser cache. Subsequent visits to the short code bypass our backend server entirely and go straight to the target URL. This completely destroys our ability to track click analytics, log IP/user-agent telemetry, enforce link expiration dates, or dynamically update target URLs. HTTP 302 Found (or 307 Temporary Redirect) ensures the browser sends every GET request to our server, guaranteeing 100% accurate click analytics."

---

### Question 2 (Intermediate): "Why Base62 encoding instead of Base64 or Hashing functions?"
**Model Answer**:
> "Base62 uses alphanumeric characters `[0-9a-zA-Z]`, which are guaranteed to be URL-safe across all HTTP clients and browsers without requiring percent-encoding (`+` and `/` in Base64 can break URL parameters). Cryptographic hashes like MD5 or SHA-256 produce long, fixed-length strings (128/256 bits) that require string truncation (e.g., taking the first 7 characters) and complex collision detection retries. Base62 encoding a 64-bit unique integer ID produces deterministic 7-character short codes ($62^7 \approx 3.52 \text{ Trillion}$ combinations) with zero collision risk."

---

### Question 3 (Advanced): "How would you design the system to handle a viral hot key receiving 100,000 requests per second?"
**Model Answer**:
> "A single viral key causes a hot-key bottleneck on a single Redis cache node. To resolve this:
> 1. **Local Worker In-Memory LRU Cache**: Application worker processes store the top 50 hot keys directly in Python application RAM (`cachetools` LRU). 95%+ of traffic is served instantly without network calls to Redis (< 0.01ms latency).
> 2. **Key Replication / Salting**: Duplicate the viral key across multiple Redis cluster nodes as `url:aB72x:1`, `url:aB72x:2`, `url:aB72x:3`. Pick a random key suffix per request to distribute network bandwidth across Redis nodes.
> 3. **Request Coalescing (Single-Flight)**: If a cache miss occurs under high load, collapse duplicate concurrent requests into a single database query using single-flight locks, preventing cache stampedes."

---

### Question 4 (Distributed Systems): "What happens if Redis goes down completely?"
**Model Answer**:
> "We implement **Graceful Degradation**. When Redis is unreachable:
> 1. The application catches Redis connection exceptions and triggers an internal Circuit Breaker to prevent thread-blocking socket timeouts.
> 2. Read queries fall back directly to PostgreSQL.
> 3. To protect PostgreSQL from crashing under 100% database read load, we activate local worker in-memory caching and apply rate limiting.
> 4. Once Redis recovers, the Circuit Breaker moves to Half-Open, verifies connectivity, and resumes normal cache population."

---

### Question 5 (Senior Principal): "How would you architect this system to scale to 10 Billion URLs and 5 Million QPS globally?"
**Model Answer**:
> "At global scale:
> 1. **Edge CDN (Cloudflare)**: Cache HTTP 302 redirects for non-expired links at 200+ edge locations worldwide. 80%+ of global reads hit CDN edge (< 5ms latency).
> 2. **Stateless API Clusters**: Scale FastAPI container nodes horizontally behind Layer 7 Load Balancers (AWS ALB).
> 3. **Redis Cluster**: Shard in-memory caching across 16+ nodes using consistent hashing.
> 4. **Database Sharding**: Partition PostgreSQL tables across 32 shards using `Hash(short_code) % 32` as the shard key.
> 5. **Async Analytics via Apache Kafka**: Redirection handlers publish click events to Kafka topics in < 1ms. Independent consumer groups write events in bulk to ClickHouse OLAP database for real-time dashboard analytics."
