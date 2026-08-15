# 16 — Analytics Pipeline & Time-Series Aggregations

## 1. Learning Objective
Learn to aggregate click streams, group clicks by hour/day/country/referrer, and optimize database read queries for analytical reporting.

---

## 2. Analytical Queries in SQL

### Group Clicks by Date
```sql
SELECT DATE(clicked_at) AS date, COUNT(*) AS clicks
FROM click_events
WHERE short_code = 'aB72x'
GROUP BY DATE(clicked_at)
ORDER BY date DESC;
```

### Top 5 Referrers
```sql
SELECT referrer, COUNT(*) AS clicks
FROM click_events
WHERE short_code = 'aB72x'
GROUP BY referrer
ORDER BY clicks DESC
LIMIT 5;
```

---

## 3. Optimizing Analytics Queries with Indexes
Without an index on `(short_code, clicked_at)`, PostgreSQL must scan every click event row across all short codes. The composite index `idx_click_events_code_time` restricts scan operations solely to rows matching `short_code`.
