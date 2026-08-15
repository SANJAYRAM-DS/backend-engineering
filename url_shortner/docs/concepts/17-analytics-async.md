# Concept 17 — Asynchronous Analytics Pipelines

# 1. Why Asynchronous Click Processing?
Synchronous database inserts during HTTP 302 redirections add 20ms-50ms disk write I/O to every user redirect.

Decouple processing:

```text
User ──> GET /aB72x ──> [ Publish Event to Queue (< 1ms) ] ──> Return 302 Redirect
                                     │
                                     ▼
                          [ Background Worker ]
                                     │
                                     ▼
                          [ Analytics Storage ]
```
