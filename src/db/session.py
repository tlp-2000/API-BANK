from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,future=True,echo = False
)

AsyncSessionLocal = sessionmaker(engine,class_=AsyncSession ,expire_on_commit=False) # type: ignore
Base = declarative_base()

#UTILITario DEPENDENCY PARA FASTAPI
async def get_async_session() -> AsyncSession: # pyright: ignore[reportInvalidTypeForm]
    async with AsyncSessionLocal() as session: # type: ignore
        yield session # type: ignore
