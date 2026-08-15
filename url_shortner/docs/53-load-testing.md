# 53 — Load Testing & Performance Profiling with Locust

## 1. Learning Objective
Execute real-world performance benchmarks using **Locust** to measure system throughput (QPS), p50/p95/p99 latency, and error rates across all 4 system architecture iterations.

---

## 2. Locust Load Testing Script (`tests/load/locustfile.py`)

```python
import random
from locust import HttpUser, task, between

class URLShortenerUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(100)
    def redirect_url(self):
        # Test 302 Redirection Latency
        self.client.get("/testCode", allow_redirects=False)

    @task(1)
    def create_url(self):
        # Test Creation Latency
        self.client.post("/api/v1/urls", json={"original_url": "https://example.com/target"})
```

---

## 3. Command Execution

```bash
locust -f tests/load/locustfile.py --headless -u 1000 -r 50 --run-time 5m --host http://localhost:8000
```
