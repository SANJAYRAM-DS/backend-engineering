# 29 — Distributed Unique ID Generation (Twitter Snowflake)

## 1. Learning Objective
Implement a distributed Snowflake ID generator that produces time-ordered, 64-bit unique integers across hundreds of API nodes without database lock coordination.

---

## 2. 64-bit Snowflake Bit Layout

```text
 1 Bit  │ 41 Bits (Timestamp in ms) │ 10 Bits (Worker ID) │ 12 Bits (Sequence)
 ───────┼───────────────────────────┼─────────────────────┼───────────────────
   0    │ 1723711800000             │ Node ID 42          │ 0 to 4095
```

---

## 3. Python Snowflake Implementation

```python
import time

class SnowflakeIDGenerator:
    def __init__(self, worker_id: int, datacenter_id: int = 1):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1

    def _time_gen(self) -> int:
        return int(time.time() * 1000)

    def generate_id(self) -> int:
        timestamp = self._time_gen()
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095
            if self.sequence == 0:
                while timestamp <= self.last_timestamp:
                    timestamp = self._time_gen()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        return (
            ((timestamp - 1704067200000) << 22)
            | (self.datacenter_id << 17)
            | (self.worker_id << 12)
            | self.sequence
        )
```
