
# app/schemas/user_statistics.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------------------- Response Schema --------------------
class UserStatisticsResponse(BaseModel):
    id: int
    user_id: int
    total_tests_attempted: int
    total_questions_practiced: int
    best_score: float
    accuracy: float
    last_test_date: Optional[datetime]

    class Config:
        orm_mode = True

# # -------------------- Create Schema (Optional) --------------------
# class UserStatisticsCreate(BaseModel):
#     user_id: int

class UserStatisticsCreate(BaseModel):
    user_id: int
    total_tests_attempted: int = 0
    total_questions_practiced: int = 0
    best_score: float = 0.0
    accuracy: float = 0.0
    last_test_date: Optional[datetime] = None


# -------------------- Update Schema --------------------
class UserStatisticsUpdate(BaseModel):
    total_tests_attempted: Optional[int] = None
    total_questions_practiced: Optional[int] = None
    best_score: Optional[float] = None
    accuracy: Optional[float] = None
    last_test_date: Optional[datetime] = None
