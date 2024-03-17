
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio

from models.entity import Base, Entity


async def main():
    # Замените DSN на свои значения
    DSN = "postgresql+asyncpg://postgres:postgres@localhost:5432/shorturl"

    engine = create_async_engine(DSN, echo=True, future=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
    
    # Дальнейшие участки кода, кроме импортов, располагайте в функции main

    # Перед закрытием приложения нужно закрыть все соединения с базой данных
    await engine.dispose()
    
asyncio.run(main())