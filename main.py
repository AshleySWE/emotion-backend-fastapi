from fastapi import FastAPI

from api.routes import note, category
from db import engine
from model.note import Base

app = FastAPI()
app.include_router(note.router)
app.include_router(category.router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)