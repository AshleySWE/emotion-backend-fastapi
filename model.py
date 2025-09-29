from supabase import create_client, Client

SUPABASE_URL = "https://nzeaqrumddjatxgodrpo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56ZWFxcnVtZGRqYXR4Z29kcnBvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjMwODg4NSwiZXhwIjoyMDY3ODg0ODg1fQ.PlBX9cG7lgpMGfpNCTlafOrhJCQS6oOTk9HK-EOKoVE"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# new_row = {
#     'title': 'ua',
#     'note': "sfsf",
#     'status': 'public',
#     'user_id': 'id'
# }
# supabase.table('Note').insert(new_row).execute()
#
#
# result = supabase.table('Note').select('*').execute()
# print(result)

from sqlalchemy import Column, String, Text, Enum as SAEnum, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum
#
Base = declarative_base()

class NoteStatusEnum(str, Enum):
    Public = "public"
    Private = "private"


class NoteDB(Base):
    __tablename__ = "Note"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    note = Column(Text, nullable=False)
    user_id = Column(Text, nullable=False)
    status = Column(SAEnum(NoteStatusEnum), nullable=False)

