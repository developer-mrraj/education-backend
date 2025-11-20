from pydantic import BaseModel, constr
from typing import Optional

class TestQuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: constr(min_length=1, max_length=1)  # type: ignore # "A","B","C","D"
    explanation: Optional[str] = None

class TestQuestionCreate(TestQuestionBase):
    pass

class TestQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_option: Optional[constr(min_length=1, max_length=1)] = None # type: ignore
    explanation: Optional[str] = None

class TestQuestionResponse(TestQuestionBase):
    id: int
    test_summary_id: int

    class Config:
        orm_mode = True
