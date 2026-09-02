# Important Execution Flows

## Flow 1: Application Startup

```text
uvicorn imports src.main:app
    |
settings load from src/core/config.py
    |
database engine exists from src/db/session.py
    |
FastAPI lifespan starts
    |
setup_logging()
    |
Base.metadata.create_all()
    |
middleware and routes are ready
```

Important functions:

- `Settings()` in `src/core/config.py`
- `create_async_engine()` in `src/db/session.py`
- `lifespan()` in `src/main.py`
- `setup_logging()` in `src/core/logging.py`

Error handling: Startup table creation catches all exceptions and silently continues. This avoids hard startup failure, but can hide real database problems.

Final output: A running FastAPI app.

## Flow 2: Create Generated Short URL

```text
POST /api/v1/urls
    |
IdempotencyAndRateLimitMiddleware
    |
URLCreateRequest validation
    |
create_short_url route
    |
get_url_service dependency
    |
URLService.create_short_url()
    |
SnowflakeIDGenerator.generate_id()
    |
encode_base62(...)[0:7]
    |
URLRepository.get_by_short_code(..., include_inactive=True)
    |
URLRepository.create_url()
    |
optional Redis SET url:{short_code}
    |
URLResponse
```

Data transformations:

- JSON request becomes `URLCreateRequest`.
- Snowflake integer becomes Base62 string.
- SQLAlchemy `URL` model becomes `URLResponse`.

Database interactions:

- Check if generated code already exists.
- Insert URL row.

External calls:

- Optional Redis `SET`.

Error handling:

- Alias/code conflict returns `409`.
- Repeated code-generation collision returns `500`.
- Redis cache failure logs warning and continues.

Final output: `201 Created` with `short_code`, `short_url`, `original_url`, timestamps, click count, and active state.

## Flow 3: Create Custom Alias

```text
POST /api/v1/urls
    |
URLCreateRequest validates custom_alias
    |
URLService.create_short_url()
    |
URLRepository.get_by_short_code(alias, include_inactive=True)
    |
if exists: 409
    |
else create URL with alias
```

Important functions:

- `validate_custom_alias()`
- `URLService.create_short_url()`
- `URLRepository.get_by_short_code()`
- `URLRepository.create_url()`

Error handling:

- Invalid alias fails validation.
- Existing alias returns `409 Conflict`.

Final output: `short_code` equals the requested alias.

## Flow 4: Redirect Short URL

```text
GET /{short_code}
    |
IdempotencyAndRateLimitMiddleware
    |
redirect_to_url()
    |
URLService.resolve_url()
    |
Redis GET url:{short_code}
    |
if hit: use cached original URL
    |
if miss: URLRepository.get_by_short_code()
    |
check expires_at
    |
optional Redis SET url:{short_code}
    |
URLRepository.increment_click_count()
    |
URLRepository.log_click_event()
    |
RedirectResponse(status_code=302)
```

Data transformations:

- Path parameter becomes `short_code`.
- Request headers become telemetry fields.
- Database URL record becomes redirect target.

Database interactions:

- Lookup URL on cache miss.
- Increment `click_count`.
- Insert `ClickEvent`.

External calls:

- Redis `GET`.
- Redis `SET` on cache miss.

Error handling:

- Missing code returns `404`.
- Expired code returns `404`.
- Redis errors log warnings and continue.
- Telemetry write errors log errors and still redirect.

Final output: `302 Found` with `Location` header pointing to original URL.

## Flow 5: Analytics

```text
GET /api/v1/urls/{short_code}/analytics
    |
middleware
    |
get_analytics route
    |
URLService.get_analytics()
    |
URLRepository.get_by_short_code()
    |
AnalyticsResponse
```

Database interactions:

- Lookup active URL by short code.

Error handling:

- Missing or inactive code returns `404`.

Final output: `200 OK` with total clicks and URL metadata.

## Flow 6: Delete URL

```text
DELETE /api/v1/urls/{short_code}
    |
middleware
    |
delete_url route
    |
URLService.delete_url()
    |
URLRepository.get_by_short_code()
    |
URLRepository.deactivate_url()
    |
optional Redis DELETE url:{short_code}
    |
204 No Content
```

Database interactions:

- Lookup active URL.
- Update `is_active=False`.

External calls:

- Optional Redis cache invalidation.

Error handling:

- Missing code returns `404`.
- Redis delete failure logs warning and continues.

Final output: `204 No Content`.

## Flow 7: Rate Limiting

```text
any request
    |
middleware dispatch()
    |
client IP calculated
    |
try Redis
    |
ZREMRANGEBYSCORE old timestamps
ZADD current timestamp
ZCARD count
EXPIRE key
    |
if count > 100: 429
    |
else continue
```

Fallback: If Redis is unavailable, a process-local Python dictionary stores recent timestamps.

Risk: In-memory fallback is not shared across workers, so it is not a real distributed limiter.

## Flow 8: Idempotent POST

```text
POST request with Idempotency-Key
    |
middleware checks Redis idempotency:{key}
    |
if cached: return cached response
    |
else route executes
    |
if response is 201:
    |
read response body
    |
store status/body in Redis for 24 hours
```

Risk: The current key does not include route or body hash, so reusing the same idempotency key with a different request could replay the wrong response.

