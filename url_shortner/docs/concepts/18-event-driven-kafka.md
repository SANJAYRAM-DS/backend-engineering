# Concept 18 — Apache Kafka & Event-Driven Architecture

# 1. Apache Kafka Fundamentals

```text
[ API Node ] ──> Kafka Producer ──> [ Topic: click_events (Partitions 0, 1, 2) ]
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     [ Consumer Group: Analytics ]                   [ Consumer Group: Fraud Scanner ]
   (Writes to Analytics Database)                   (Blocks Malicious Bot IPs)
```

- **Topics & Partitions**: Distributed append-only commit logs partitioned for parallel consumer throughput.
- **Consumer Groups**: Independent microservices read from topic offsets without altering data.
- **Delivery Semantics**: **At-Least-Once** guarantees no event is lost during worker failures.
