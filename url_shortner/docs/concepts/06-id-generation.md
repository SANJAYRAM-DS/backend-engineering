# Concept 06 — Short Code & ID Generation Strategies

# 1. Four Core ID Generation Approaches

| Approach | Mechanics | Advantages | Disadvantages | Collision Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Random Strings** | Generate random 7-char string `aB72x` | Simple, independent | Requires database pre-lookup retry loop | High at scale |
| **Hash Truncation (MD5/SHA256)** | Take first 7 chars of `MD5(url)` | Deterministic mapping | Collision risk, requires retry | Moderate |
| **DB Auto-Increment + Base62** | Convert 64-bit DB ID (`125 -> 21`) | Zero collision, compact | Predictable sequential IDs | Zero |
| **Distributed Snowflake ID + Base62** | 64-bit (Timestamp + WorkerID + Sequence) | Distributed, zero DB lock, time-ordered | Requires worker ID coordination | Zero |

---

# 2. Key Takeaway
Combining a **64-bit integer ID** with **Base62 encoding** produces guaranteed unique, non-colliding short codes!
