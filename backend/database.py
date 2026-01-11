from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import APP_DB_URL

engine = create_async_engine(APP_DB_URL)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_factory() as session:
        yield session
