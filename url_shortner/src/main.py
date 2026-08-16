from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from src.core.config import settings
from src.core.logging import setup_logging
from src.db.session import engine, Base
from src.core.redis import close_redis_client
from src.api.v1.urls import router as urls_router
from src.services.url_service import URLService
from src.api.deps import get_url_service
from src.api.middleware import IdempotencyAndRateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    # Create DB tables if they don't exist
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        pass
    yield
    await engine.dispose()
    await close_redis_client()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(IdempotencyAndRateLimitMiddleware)

# Register API routers
app.include_router(urls_router, prefix=settings.API_V1_STR)


@app.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    request: Request,
    url_service: URLService = Depends(get_url_service),
):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    target_url = await url_service.resolve_url(
        short_code=short_code,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
    )
    return RedirectResponse(url=target_url, status_code=302)