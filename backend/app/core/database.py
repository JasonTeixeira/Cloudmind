"""
Production-ready database module for CloudMind
"""

import asyncio
import logging
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import text
from sqlalchemy.orm import declarative_base

from app.core.config import settings
from app.core.monitoring import record_database_query

logger = logging.getLogger(__name__)

# Database engine
engine = None
AsyncSessionLocal = None

# SQLAlchemy Base
Base = declarative_base()

async def init_db():
    """Initialize database connection"""
    global engine, AsyncSessionLocal
    
    try:
        logger.info("Initializing database connection...")
        
        # Create async engine with connection pooling
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_timeout=30
        )
        
        # Create session factory
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
        
        # Test connection
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("✅ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

async def close_db():
    """Close database connections"""
    global engine
    
    try:
        if engine:
            await engine.dispose()
            logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def test_db_connection() -> bool:
    """Test database connection"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            await result.fetchone()
            record_database_query("test_connection")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

async def get_db_stats() -> dict:
    """Get database statistics"""
    try:
        async with AsyncSessionLocal() as session:
            # Get connection pool stats
            pool = engine.pool
            stats = {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "invalid": pool.invalid()
            }
            
            # Get table counts
            tables = ["users", "projects", "security_scans", "cost_analyses"]
            table_counts = {}
            
            for table in tables:
                try:
                    result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    table_counts[table] = count
                except Exception:
                    table_counts[table] = 0
            
            stats["table_counts"] = table_counts
            record_database_query("get_stats")
            
            return stats
            
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {"error": str(e)} 