# 44 — Idempotency Keys & Safe API Retries

## 1. Learning Objective
Design idempotent `POST /api/v1/urls` API endpoints using `Idempotency-Key` HTTP headers to guarantee client network retries never duplicate resources.

---

## 2. Idempotency Flow

```text
[ Client ] ──> POST /api/v1/urls (Header: Idempotency-Key: 7b9e02c1...)
                     │
                     ▼
        [ Check Redis Key "idempotency:7b9e02c1..." ]
                     │
         ┌───────────┴───────────┐
         │                       │
 [ Key Exists ]            [ Key Missing ]
         │                       │
         ▼                       ▼
 [ Return Cached Response ] [ Execute Creation & Store Response in Redis ]
```

---

## 3. Implementation Middleware

```python
async def idempotency_middleware(request: Request, call_next):
    key = request.headers.get("Idempotency-Key")
    if not key or request.method != "POST":
        return await call_next(request)

    redis_key = f"idempotency:{key}"
    cached_res = await redis_client.get(redis_key)
    if cached_res:
        data = json.loads(cached_res)
        return JSONResponse(status_code=data["status"], content=data["body"])

    response = await call_next(request)
    if response.status_code == 201:
        body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(body))
        await redis_client.set(redis_key, json.dumps({"status": 201, "body": json.loads(body[0])}), ex=86400)

    return response
```
