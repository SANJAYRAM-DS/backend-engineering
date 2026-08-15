# 32 — Apache Kafka Integration & Delivery Semantics

## 1. Learning Objective
Master Apache Kafka architecture: Topics, Partitions, Producers, Consumer Groups, Offsets, and Delivery Semantics (At-Least-Once, At-Most-Once, Exactly-Once).

---

## 2. Kafka Architecture Blueprint

```text
[ API Node ] ──> Kafka Producer ──> [ Topic: click_events (3 Partitions) ]
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     [ Consumer Group: Analytics ]                   [ Consumer Group: Fraud Detection ]
   (Writes to Analytics Database)                   (Scans for Malicious Bot Attacks)
```

---

## 3. Kafka Producer Code Snippet (`src/messaging/kafka_producer.py`)

```python
import json
from aiokafka import AIOKafkaProducer

class ClickEventProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_click_event(self, short_code: str, ip: str, user_agent: str):
        payload = {
            "short_code": short_code,
            "ip_address": ip,
            "user_agent": user_agent,
            "timestamp": int(time.time()),
        }
        await self.producer.send_and_wait("click_events", payload)
```
