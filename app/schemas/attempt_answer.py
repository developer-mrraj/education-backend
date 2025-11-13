from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Create AttemptAnswer ---
class AttemptAnswerCreate(BaseModel):
    attempt_id: int
    question_id: int
    selected_option: str
    is_correct: str

# --- Update AttemptAnswer ---
class AttemptAnswerUpdate(BaseModel):
    attempt_id: Optional[int] = None
    question_id: Optional[int] = None
    selected_option: Optional[str] = None
    is_correct: Optional[bool] = None

# --- Response Schema ---
class AttemptAnswerResponse(BaseModel):
    answer_id: int
    attempt_id: int
    question_id: int
    selected_option: str
    is_correct: bool

    class Config:
        orm_mode = True
