from enum import Enum
from typing import List

from fastapi import Depends, Query, HTTPException, Path, Body, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from crud.note import create_note, get_notes_by_user
from db import get_db
from model.note import NoteDB
from schema.note import NoteCreate, NoteUpdate


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/notes/", response_model=NoteCreate)
async def post_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    return await create_note(db, note)


# TODO: get_note 的 api 加 comment_id
@router.get("/", response_model=List[NoteCreate])
async def get_notes(
        user_id: str = Query(..., description="Filter notes by user_id"),
        db: AsyncSession = Depends(get_db)
):
    try:
        return await get_notes_by_user(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


# TODO Swagger 上面不會出現 user_id 需要 debug
@router.put("/notes/{note_id}", response_model=NoteUpdate)
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
