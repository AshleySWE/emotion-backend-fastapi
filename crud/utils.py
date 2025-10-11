from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from main import app


# Testing for the server connection
@app.get("/time")
async def root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT NOW()"))
    now = result.scalar()
    return {"db_time": str(now)}