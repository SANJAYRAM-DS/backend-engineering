from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Determine Database URL (Default to PostgreSQL, or SQLite async fallback for local dev)
DATABASE_URL = settings.DATABASE_URL or f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Determine engine configuration based on database driver
is_sqlite = DATABASE_URL.startswith("sqlite")

engine_args = {}
if not is_sqlite:
    engine_args = {
        "pool_size": 10,        # Keep up to 10 persistent DB connections in pool
        "max_overflow": 20,     # Allow up to 20 extra temporary connections under heavy load
        "pool_pre_ping": True,  # Test connection health before handing to a request (handles stale sockets)
    }

# 1. Create Async Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG, # Log raw SQL queries in DEBUG mode
    **engine_args
)

# 2. Create Async Session Factory (Unit of Work)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 3. FastAPI Dependency: Yields 1 DB session per HTTP request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
