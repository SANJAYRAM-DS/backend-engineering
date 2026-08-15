# 35 — Concurrency Control: Optimistic vs Pessimistic Locking

## 1. Learning Objective
Master database locking mechanisms to prevent race conditions during concurrent link updates or alias creation.

---

## 2. Locking Patterns

### Pessimistic Locking (`SELECT FOR UPDATE`)
Locks the row in PostgreSQL until the transaction commits, blocking all concurrent read/write locks:
```sql
SELECT * FROM urls WHERE short_code = 'my-sale' FOR UPDATE;
```

### Optimistic Locking (Version Column)
Does not lock database rows. Instead, checks `version` on `UPDATE`:
```sql
UPDATE urls 
SET click_count = click_count + 1, version = version + 1
WHERE short_code = 'my-sale' AND version = 4;
```
If 0 rows were updated, a concurrent transaction modified the row—retry operation!
