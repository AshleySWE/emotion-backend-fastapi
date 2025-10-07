from enum import Enum
from typing import List

from fastapi import FastAPI, Depends, Query, HTTPException, Path, Body
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from crud import create_note
from db import get_db, engine
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from model import Base, NoteDB
from schemas import NoteCreate, NoteUpdate

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/notes/", response_model=NoteCreate)
async def post_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    return await create_note(db, note)


@app.get("/notes", response_model=List[NoteCreate])
async def get_notes(
    user_id: str = Query(..., description="Filter notes by user_id"),
    db: AsyncSession = Depends(get_db)
) -> List[NoteCreate]:
    try:
        result = await db.execute(
            select(NoteDB).where(NoteDB.user_id == user_id)
        )
        notes = result.scalars().all()
        return [NoteCreate.from_orm(note) for note in notes]
    except Exception as e:
        raise HTTPException(status_code=500, detail= repr(e))


# TODO Swagger 上面不會出現 user_id 需要 debug
@app.put("/notes/{note_id}", response_model=NoteUpdate)
async def update_note(
    note_id: str = Path(..., description="Note ID to update"),
    update_data: NoteUpdate = Body(..., description="Note update payload"),
    db: AsyncSession = Depends(get_db)
):
    # 從 body 取得 user_id
    user_id = update_data.user_id

    # 查找該使用者的 note
    result = await db.execute(
        select(NoteDB).where(NoteDB.id == note_id, NoteDB.user_id == user_id)
    )
    note = result.scalars().first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found or access denied")

    note.id = '20'
    # 更新欄位
    if update_data.title is not None:
        note.title = update_data.title
    if update_data.note is not None:
        note.note = update_data.note
    if update_data.status is not None:
        note.status = update_data.status

    await db.commit()
    await db.refresh(note)

    return note

# -----------------------------------------------------------------------


@app.get("/time")
async def root(db: AsyncSession = Depends(get_db)):
    # 測試連線：查詢 PostgreSQL 伺服器時間
    result = await db.execute(text("SELECT NOW()"))
    now = result.scalar()
    return {"db_time": str(now)}


# 編輯 note （用 dict 存放 id -> Note）
# 填情緒文字
class NoteStatus(str, Enum):
    Public = "public"
    Private = "private"


class Note(BaseModel):
    id: str
    title: str = None
    note: str
    status: NoteStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


fake_db: dict[str, Note] = {}


@app.get("/home")
def home():
    return 'ah'


# 將前端的 notes 存到後端 DB
# @app.post("/notes")
# def create_notes(notes: list[Note]):
#     pass


# @app.put("/notes")
# def update_note(update_note: Note):
#     fake_db[update_note.id]
@app.put("/notes/{note_id}")
def update_note(note_id: str, update_note: Note):
    fake_db[update_note.id]


class Category(str, Enum):
    family = "family"
    career = "career"
    society = "society"


@app.get("/category", response_model=List[Category])
async def get_category() -> List[Category]:
    return [Category.family, Category.career, Category.society]


# TODO: get_note 的 api 加 comment_id

class Comment(BaseModel):
    id: int
    comment: str
    user_id: str
    upload_time: datetime


fake_comments = [
    Comment(
        id=1,
        comment="Hi",
        user_id='a1',
        upload_time=datetime.now()
    ),
    Comment(
        id=2,
        comment="Hi",
        user_id='a1',
        upload_time=datetime.now()
    ),
    Comment(
        id=3,
        comment="Hi",
        user_id='a1',
        upload_time=datetime.now()
    )
]


@app.get("/comment", response_model=List[Comment])
async def get_comments() -> List[Comment]:
    return sorted(fake_comments, key=lambda comment: comment.upload_time, reverse=True)
