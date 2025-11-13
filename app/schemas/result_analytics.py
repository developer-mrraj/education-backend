from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Create ResultAnalytics ---
class ResultAnalyticsCreate(BaseModel):
    attempt_id: int
    total_questions: int
    total_correct: int
    total_wrong: int
    total_unattempted: int
    accuracy: float
    percentage: float

# --- Update ResultAnalytics ---
class ResultAnalyticsUpdate(BaseModel):
    attempt_id: Optional[int] = None
    total_questions: Optional[int] = None
    total_correct: Optional[int] = None
    total_wrong: Optional[int] = None
    total_unattempted: Optional[int] = None
    accuracy: Optional[float] = None
    percentage: Optional[float] = None

# --- Response Schema ---
class ResultAnalyticsResponse(BaseModel):
    result_id: int
    attempt_id: int
    total_questions: int
    total_correct: int
    total_wrong: int
    total_unattempted: int
    accuracy: float
    percentage: float
    created_at: datetime

    class Config:
        orm_mode = True
