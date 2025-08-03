from enum import Enum
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, timezone

app = FastAPI()


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
@app.post("/notes")
def create_notes(notes: list[Note]):
    pass


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
