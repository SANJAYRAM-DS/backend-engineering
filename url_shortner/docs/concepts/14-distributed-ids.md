# Concept 14 — Distributed ID Generation (Twitter Snowflake)

# 1. The Distributed Counter Collision Problem
If multiple stateless API nodes (API 1, API 2, API 3) generate sequential IDs independently without database lock coordination:

- API 1 generates ID `100` -> `1C`
- API 2 generates ID `100` -> `1C`

Collision occurs!

---

# 2. Twitter Snowflake 64-bit ID Generation

```text
 1 Bit  │ 41 Bits (Timestamp in ms) │ 10 Bits (Worker ID) │ 12 Bits (Sequence)
 ───────┼───────────────────────────┼─────────────────────┼───────────────────
   0    │ 1723711800000             │ Node ID 42          │ 0 to 4095
```

- **41 Bits Timestamp**: Supports 69 years of millisecond-ordered IDs.
- **10 Bits Worker ID**: Supports up to 1,024 independent API worker nodes.
- **12 Bits Sequence**: Supports up to 4,096 IDs per millisecond per worker node!
- **Result**: Zero DB lock coordination, time-ordered, globally unique integer IDs.
