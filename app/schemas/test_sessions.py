
# app/schemas/test_sessions.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# When starting a session
class TestSessionCreate(BaseModel):
   pass


# When ending a session
class TestSessionEnd(BaseModel):
    pass  # no fields because only completed_at is updated automatically


# Response schema
class TestSessionResponse(BaseModel):
    id: int
    user_id: int
    test_series_id: int
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True
