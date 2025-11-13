from pydantic import BaseModel
from typing import Optional

# --- Create Question ---
class QuestionCreate(BaseModel):
    test_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    marks: int = 1

# --- Update Question ---
class QuestionUpdate(BaseModel):
    test_id: Optional[int] = None
    question_text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_option: Optional[str] = None
    marks: Optional[int] = None

# --- Response Schema ---
class QuestionResponse(BaseModel):
    question_id: int
    test_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    marks: int

    class Config:
        orm_mode = True
