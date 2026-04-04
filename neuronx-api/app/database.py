"""
Database connection and session management.
Uses SQLAlchemy async with asyncpg for PostgreSQL on Railway.

If DATABASE_URL is not set, database features are disabled gracefully —
the API continues to work without persistence (GHL remains source of truth).
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

logger = logging.getLogger("neuronx.database")

engine = None
async_session_factory = None


class Base(DeclarativeBase):
    pass


def is_db_configured() -> bool:
    return bool(settings.database_url)


async def init_db():
    """Initialize database engine and create tables. Call on app startup."""
    global engine, async_session_factory

    if not is_db_configured():
        logger.warning("DATABASE_URL not set — running without database persistence")
        return

    # Railway provides DATABASE_URL as postgres:// but asyncpg needs postgresql+asyncpg://
    db_url = settings.database_url
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(db_url, echo=False, pool_size=5, max_overflow=10)
    async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create tables
    async with engine.begin() as conn:
        from app.models.db_models import Base as DBBase  # noqa: F811
        await conn.run_sync(DBBase.metadata.create_all)

    logger.info("Database initialized successfully")


async def close_db():
    """Close database engine. Call on app shutdown."""
    global engine
    if engine:
        await engine.dispose()
        logger.info("Database connection closed")


async def get_session() -> AsyncSession:
    """Get a database session. Use as async context manager."""
    if not async_session_factory:
        raise RuntimeError("Database not initialized. Set DATABASE_URL env var.")
    async with async_session_factory() as session:
        yield session
