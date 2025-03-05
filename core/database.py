from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import DATABASE_URL

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base Model
Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with async_session_maker() as session:
        yield session
