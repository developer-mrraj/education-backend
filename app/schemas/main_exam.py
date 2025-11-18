# schemas/main_exam.py

from pydantic import BaseModel
from typing import Optional


# -------------------------
# Base Schema
# -------------------------
class MainExamBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
   

    price: Optional[int] = None
    is_free: bool = False

    button_text: Optional[str] = None
    description: Optional[str] = None

    total_tests: int

    logo_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    is_active: bool = True


# -------------------------
# Create Schema
# -------------------------
class MainExamCreate(MainExamBase):
    pass


# -------------------------
# Update Schema
# -------------------------
class MainExamUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    tagline: Optional[str] = None

    price: Optional[int] = None
    is_free: Optional[bool] = None

    button_text: Optional[str] = None
    description: Optional[str] = None

    total_tests: Optional[int] = None

    logo_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    is_active: Optional[bool] = None


# -------------------------
# Response Schema
# -------------------------
class MainExamResponse(MainExamBase):
    id: int

    class Config:
        from_attributes = True
