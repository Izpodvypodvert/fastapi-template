from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from app.core.config import settings


engine: AsyncEngine = create_async_engine(settings.database_url, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session

