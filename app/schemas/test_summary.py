from pydantic import BaseModel
from typing import Optional, List


# --------------------------
# Base Schema (Common fields)
# --------------------------
class TestSummaryBase(BaseModel):
   
    section_name: str
    questions: int
    marks: int
    duration: int


# --------------------------
# Create Schema
# --------------------------
class TestSummaryCreate(TestSummaryBase):
    pass


# --------------------------
# Update Schema
# --------------------------
class TestSummaryUpdate(BaseModel):
    section_name: Optional[str] = None
    questions: Optional[int] = None
    marks: Optional[int] = None
    duration: Optional[int] = None


# --------------------------
# Response Schema
# --------------------------
class TestSummaryResponse(TestSummaryBase):
    id: int
    test_series_id: int
    total_questions: int
    total_marks: int
    total_duration: int

    class Config:
        orm_mode = True
