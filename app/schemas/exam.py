from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- Create Exam ---
class ExamCreate(BaseModel):
    exam_name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None

# --- Update Exam ---
class ExamUpdate(BaseModel):
    exam_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None

# --- Response Schema ---
class ExamResponse(BaseModel):
    exam_id: int
    exam_name: str
    description: Optional[str]
    logo_url: Optional[str]

    class Config:
        orm_mode = True
