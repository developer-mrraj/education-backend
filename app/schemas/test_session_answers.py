
# app/schemas/test_session_answers.py
from pydantic import BaseModel, Field
from typing import Annotated

# -------------------- Input Schema for Creating an Answer --------------------
class TestSessionAnswerCreate(BaseModel):
    # session_id: int
    # question_id: int
    user_answer: Annotated[str, Field(pattern="^[A-Da-d]$", description="Answer must be A, B, C, or D")]

# -------------------- Input Schema for Updating an Answer --------------------
class TestSessionAnswerUpdate(BaseModel):
    user_answer: Annotated[str, Field(pattern="^[A-Da-d]$", description="Answer must be A, B, C, or D")]

# -------------------- Response Schema --------------------
class TestSessionAnswerResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    user_answer: str
    is_correct: bool

    class Config:
        orm_mode = True
