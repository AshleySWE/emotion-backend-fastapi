from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, timezone

app = FastAPI()

@app.get("/home")
def home():
    return 'ah'

# 填情緒文字

class Note(BaseModel):
    id: str
    title: str = None
    content: str
    upload_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# 將前端的 notes 存到後端 DB
@app.post("/notes")
def create_notes(notes: list[Note]):
    pass

# 編輯 note （用 dict 存放 id -> Note）
fake_db: dict[str, Note] = {}
# @app.put("/notes")
# def update_note(update_note: Note):
#     fake_db[update_note.id]
@app.put("/notes/{note_id}")
def update_note(note_id: str, update_note: Note):
    fake_db[update_note.id]


# @app.get("/category")
# def get_category():
#     id: 
#     return 'ah'

