import json
import time
from typing import Callable, Dict
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.redis import get_redis_client

# In-memory rate limiting fallback cache
in_memory_rate_limit: Dict[str, list] = {}


class IdempotencyAndRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"

        # 1. Rate Limiting (Sliding Window Log: max 100 requests per 60 seconds)
        window_seconds = 60
        max_requests = 100
        now = time.time()
        redis = await get_redis_client()

        if redis:
            try:
                key = f"rate_limit:{client_ip}"
                clear_before = now - window_seconds
                async with redis.pipeline(transaction=True) as pipe:
                    pipe.zremrangebyscore(key, 0, clear_before)
                    pipe.zadd(key, {str(now): now})
                    pipe.zcard(key)
                    pipe.expire(key, window_seconds)
                    results = await pipe.execute()
                request_count = results[2]
                if request_count > max_requests:
                    return JSONResponse(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={"detail": "Rate limit exceeded. Please try again later."},
                    )
            except Exception:
                pass
        else:
            # Fallback in-memory rate limiting
            history = in_memory_rate_limit.setdefault(client_ip, [])
            in_memory_rate_limit[client_ip] = [t for t in history if now - t < window_seconds]
            if len(in_memory_rate_limit[client_ip]) >= max_requests:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Please try again later."},
                )
            in_memory_rate_limit[client_ip].append(now)

        # 2. Idempotency Key Handling for POST requests
        idempotency_key = request.headers.get("Idempotency-Key")
        if request.method == "POST" and idempotency_key and redis:
            cache_key = f"idempotency:{idempotency_key}"
            try:
                cached_resp = await redis.get(cache_key)
                if cached_resp:
                    data = json.loads(cached_resp)
                    return JSONResponse(
                        status_code=data["status_code"], content=data["body"]
                    )
            except Exception:
                pass

        response = await call_next(request)

        # Cache successful POST response if Idempotency-Key was provided
        if (
            request.method == "POST"
            and idempotency_key
            and redis
            and response.status_code == 201
        ):
            try:
                body_bytes = [chunk async for chunk in response.body_iterator]
                # Re-assign body_iterator so response payload can be transmitted to client
                async def iterate_body():
                    for chunk in body_bytes:
                        yield chunk

                response.body_iterator = iterate_body()
                if body_bytes:
                    body_json = json.loads(body_bytes[0].decode("utf-8"))
                    cache_key = f"idempotency:{idempotency_key}"
                    await redis.set(
                        cache_key,
                        json.dumps({"status_code": 201, "body": body_json}),
                        ex=86400,
                    )
            except Exception:
                pass

        return response
