# 39 — CAP Theorem & PACELC Theorem Applied

## 1. Learning Objective
Apply the CAP Theorem (Consistency, Availability, Partition Tolerance) and PACELC Theorem to real-world URL shortener architectural choices.

---

## 2. CAP Theorem Realities

In the presence of a Network Partition ($P$), a distributed system must choose between:
- **Consistency ($C$)**: Refuse writes/reads if state cannot be guaranteed (CP).
- **Availability ($A$)**: Accept writes/reads even if data might be stale (AP).

```text
               [ Network Partition Occurs ]
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    [ CP Choice: Fail ]            [ AP Choice: Serve ]
   (Return 500 error to           (Return cached target,
    guarantee consistency)         accept eventual lag)
```

> **URL Shortener Decision:** For **Redirection Traffic**, we choose **AP** (High Availability over strict immediate consistency). For **Custom Alias Creation**, we choose **CP** (Consistency over Availability).
