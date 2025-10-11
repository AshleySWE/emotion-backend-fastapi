from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.note import NoteDB
from schema.note import NoteCreate


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
    return note_db


async def get_notes_by_user(db: AsyncSession, user_id: str) -> List[NoteCreate]:
    try:
        result = await db.execute(
            select(NoteDB).where(NoteDB.user_id == user_id)
        )
        notes = result.scalars().all()
    except Exception as e:
        print("Error WTF:", e)
        await db.rollback()

    return [NoteCreate.from_orm(note) for note in notes]