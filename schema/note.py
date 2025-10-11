from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum


class NoteStatus(str, Enum):
    Public = "public"
    Private = "private"


class NoteCreate(BaseModel):
    title: str
    note: str
    user_id: str
    status: NoteStatus

    class Config:
        orm_mode = True
        from_attributes = True


class Note(BaseModel):
    id: str
    title: str = None
    note: str
    status: NoteStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NoteUpdate(BaseModel):
    user_id: str          # 放在 body，驗證使用者身分
    title: Optional[str] = None
    note: Optional[str] = None
    status: Optional[NoteStatus] = None

    class Config:
        from_attributes = True
