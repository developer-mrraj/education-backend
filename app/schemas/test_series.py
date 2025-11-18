# schemas/test_series_list.py

from pydantic import BaseModel
from typing import Optional


# -------------------------
# Base Schema
# -------------------------
class TestSeriesListBase(BaseModel):
    sub_exam_id: int

    series_number: int
    title: str
    duration_minutes: int
    total_questions: int

    is_active: bool = True


# -------------------------
# Create Schema
# -------------------------
class TestSeriesListCreate(TestSeriesListBase):
    pass


# -------------------------
# Update Schema
# -------------------------
class TestSeriesListUpdate(BaseModel):
    sub_exam_id: Optional[int] = None

    series_number: Optional[int] = None
    title: Optional[str] = None
    duration_minutes: Optional[int] = None
    total_questions: Optional[int] = None

    is_active: Optional[bool] = None


# -------------------------
# Response Schema
# -------------------------
class TestSeriesListResponse(TestSeriesListBase):
    id: int

    class Config:
        from_attributes = True
