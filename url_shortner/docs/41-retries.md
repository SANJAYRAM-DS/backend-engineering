# 41 & 42 — Retries, Exponential Backoff, and Jitter

## 1. Learning Objective
Implement intelligent retry policies with Exponential Backoff and Full Jitter to prevent **Retry Storms** (Thundering Herd) against recovering databases.

---

## 2. Mathematical Backoff with Jitter Formula

$$\text{Sleep Time} = \text{random}(0, \min(\text{MAX\_BACKOFF}, \text{BASE} \times 2^{\text{attempt}}))$$

```python
import asyncio
import random

async def execute_with_retry(func, max_attempts=3, base_delay=0.1, max_delay=2.0):
    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            sleep_time = random.uniform(0, min(max_delay, base_delay * (2 ** attempt)))
            await asyncio.sleep(sleep_time)
```
