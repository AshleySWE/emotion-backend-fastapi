import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

# 從環境變數讀取 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 建立 async SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# 依需求生成 Session
async def get_db():
    async with async_session() as session:
        yield session
