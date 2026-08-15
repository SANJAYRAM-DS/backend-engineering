# 36 — Race Conditions & Alias Claim Conflicts

## 1. Learning Objective
Reproduce a race condition where two concurrent users request the same custom alias `short.ly/flash-sale` at the exact same millisecond, and resolve it using PostgreSQL unique constraints.

---

## 2. Race Condition Sequence

```text
User A: [ Check Alias "flash-sale" ] ──(DB Says: Free)──> [ Attempts Insert ]
User B: [ Check Alias "flash-sale" ] ──(DB Says: Free)──> [ Attempts Insert ]
                                                                 │
                                                       [ Unique Index Prevents ]
                                                       [ Second Insert Failure ]
```
