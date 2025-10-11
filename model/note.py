from sqlalchemy import Column, String, Text, Enum as SAEnum, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
#
Base = declarative_base()


class NoteStatus(str, Enum):
    Public = "public"
    Private = "private"


class NoteDB(Base):
    __tablename__ = "Note"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    note = Column(Text, nullable=False)
    user_id = Column(Text, nullable=False)
    status = Column(SAEnum(NoteStatus), nullable=False)



