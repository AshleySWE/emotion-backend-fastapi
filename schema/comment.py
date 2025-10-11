from datetime import datetime
from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    comment: str
    user_id: str
    upload_time: datetime
