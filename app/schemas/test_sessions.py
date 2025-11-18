# app/schemas/test_sessions.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TestSessionCreate(BaseModel):
    user_id: int
    test_series_id: int
    total_questions: int

class TestSessionEnd(BaseModel):
    attempted: int
    correct: int
    wrong: int
    score: float
    completed_at: Optional[datetime] = None

class TestSessionResponse(BaseModel):
    id: int
    user_id: int
    test_series_id: int
    started_at: datetime
    completed_at: Optional[datetime]
    total_questions: int
    attempted: int
    correct: int
    wrong: int
    score: float
    accuracy: float

    class Config:
        orm_mode = True
