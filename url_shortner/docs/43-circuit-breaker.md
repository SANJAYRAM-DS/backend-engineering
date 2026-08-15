# 43 — Circuit Breakers (Resilience Patterns)

## 1. Learning Objective
Implement the Circuit Breaker pattern (Closed -> Open -> Half-Open) to fail fast when Redis or external APIs become unresponsive.

---

## 2. Circuit Breaker State Machine

```text
[ CLOSED (Normal) ] ──(5 Consecutive Failures)──> [ OPEN (Fail Fast) ]
        ▲                                                │
        │                                         (30s Timeout)
        │                                                │
        └───────────── [ HALF-OPEN (Test Query) ] <──────┘
```

---

## 3. Implementation Concept

```python
class CircuitBreakerOpenException(Exception): pass

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=30):
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()

    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_state_change > 30:
                self.state = "HALF-OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit open: Fast failing request")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= 5:
                self.state = "OPEN"
                self.last_state_change = time.time()
            raise e
```
