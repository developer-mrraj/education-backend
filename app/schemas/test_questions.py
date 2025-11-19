# from pydantic import BaseModel, Field
# from typing import Optional


# # -------------------- Base Schema --------------------
# class TestQuestionBase(BaseModel):
#     question_text: str

#     option_a: str
#     option_b: str
#     option_c: str
#     option_d: str

#     correct_option: str = Field(pattern="^[A-D]$")

#     explanation: Optional[str] = None

#     test_summary_id: int   # FK


# # -------------------- Create Schema --------------------
# class TestQuestionCreate(TestQuestionBase):
#     pass


# # -------------------- Update Schema --------------------
# class TestQuestionUpdate(BaseModel):
#     question_text: Optional[str] = None

#     option_a: Optional[str] = None
#     option_b: Optional[str] = None
#     option_c: Optional[str] = None
#     option_d: Optional[str] = None

#     correct_option: Optional[str] = Field(default=None, pattern="^[A-D]$")

#     explanation: Optional[str] = None

#     test_summary_id: Optional[int] = None


# # -------------------- Response Schema --------------------
# class TestQuestionResponse(TestQuestionBase):
#     id: int

#     class Config:
#         from_attributes = True


# app/schemas/test_questions.py
from pydantic import BaseModel, constr
from typing import Optional

# Base schema - used for create/update
class TestQuestionBase(BaseModel):
    test_summary_id: int
    section_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: constr(min_length=1, max_length=1)  # type: ignore # "A"|"B"|"C"|"D"
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
    section_id: Optional[int] = None

class TestQuestionResponse(TestQuestionBase):
    id: int

    class Config:
        orm_mode = True
