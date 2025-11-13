from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Create Test ---
class TestCreate(BaseModel):
    category_id: int
    test_name: str
    total_questions: int
    total_marks: int
    duration_minutes: int
    price: float = 0.0
    is_free: bool = True

# --- Update Test ---
class TestUpdate(BaseModel):
    category_id: Optional[int] = None
    test_name: Optional[str] = None
    total_questions: Optional[int] = None
    total_marks: Optional[int] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    is_free: Optional[bool] = None

# --- Response Schema ---
class TestResponse(BaseModel):
    test_id: int
    category_id: int
    test_name: str
    total_questions: int
    total_marks: int
    duration_minutes: int
    price: float
    is_free: bool

    class Config:
        orm_mode = True
