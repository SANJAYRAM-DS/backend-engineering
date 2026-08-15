# 31 — Message Queues & Asynchronous Processing Patterns

## 1. Learning Objective
Compare Message Queues (RabbitMQ, AWS SQS) vs Distributed Commit Logs (Apache Kafka) for asynchronous task processing.

---

## 2. Queue Architectural Models

- **Point-to-Point Message Queue (RabbitMQ)**: Producer pushes task to queue; single worker consumes and deletes message.
- **Publish/Subscribe Distributed Log (Kafka)**: Producer writes event to topic partition log; multiple independent consumer groups read and retain events for replay.
