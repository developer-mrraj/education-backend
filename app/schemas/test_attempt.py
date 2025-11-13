from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Create TestAttempt ---
class TestAttemptCreate(BaseModel):
    user_id: int
    test_id: int
    # Optional fields not provided by user; backend will handle defaults
    start_time: Optional[datetime] = None  # will default to current timestamp
    end_time: Optional[datetime] = None    # will remain null until test is finished
    score: Optional[int] = None            # will remain null until test is finished
    status: Optional[str] = None           # default "in_progress"

# --- Update TestAttempt ---
class TestAttemptUpdate(BaseModel):
    user_id: Optional[int] = None
    test_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    score: Optional[int] = None
    status: Optional[str] = None  # e.g., "in_progress", "completed"

# --- Response Schema ---
class TestAttemptResponse(BaseModel):
    attempt_id: int
    user_id: int
    test_id: int
    start_time: datetime
    end_time: Optional[datetime]
    score: Optional[int]
    status: str

    class Config:
        orm_mode = True
