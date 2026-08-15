# 09 — URL Redirection & Telemetry Capture

## 1. Learning Objective
Understand high-throughput URL redirection processing, click metric tracking, and header extraction (`User-Agent`, `Referer`, Client IP).

---

## 2. HTTP Redirection Flow

```text
Client GET /aB72x
  │
  ├─> Read DB/Cache ──> Check is_active & expires_at
  │                          │
  ├─> Log Click Event <──────┘
  │
  └─> Return HTTP 302 Location: https://target.com
```

---

## 3. Extracting Header Telemetry in FastAPI

```python
@app.get("/{short_code}")
async def redirect(short_code: str, request: Request, service: URLService = Depends()):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")
    
    target_url = await service.resolve_url(short_code, ip, user_agent, referrer)
    return RedirectResponse(url=target_url, status_code=302)
```
