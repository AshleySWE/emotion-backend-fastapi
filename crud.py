from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from model import NoteDB
from schemas import NoteCreate


async def create_note(db: AsyncSession, note: NoteCreate) -> NoteDB:
    note_db = NoteDB(
        title=note.title,
        note=note.note,
        status=note.status,
        user_id=note.user_id
    )
    db.add(note_db)
    try:
        await db.commit()
        await db.refresh(note_db)
    except Exception as e:
        print("Error WTF:", e)
        await db.rollback()
        raise HTTPException(status_code=400, detail="Note with this ID already exists")
    return note_db
