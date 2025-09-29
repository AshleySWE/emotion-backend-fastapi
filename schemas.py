from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum

from model import NoteStatusEnum


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


class NoteUpdate(BaseModel):
    user_id: str          # 放在 body，驗證使用者身分
    title: Optional[str] = None
    note: Optional[str] = None
    status: Optional[NoteStatusEnum] = None
    class Config:
        orm_mode = True
        from_attributes = True
