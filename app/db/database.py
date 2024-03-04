from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.future import select
from app.db.models.client import Client
from app.db.base import Base
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_ADDRESS')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # Set echo=True for debugging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_context(file_path):
    async with engine.begin() as conn:
        stmt = select(Client)
        result = await conn.execute(stmt)
        if not result.fetchall():
            with open(file_path, 'r') as file:
                query = text(file.read())
                await conn.execute(query)
