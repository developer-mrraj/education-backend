# app/schemas/category.py
from pydantic import BaseModel
from typing import Optional

# --- Create Category ---
class CategoryCreate(BaseModel):
    exam_id: int
    category_name: str
    description: Optional[str] = None

# --- Update Category ---
class CategoryUpdate(BaseModel):
    exam_id: Optional[int] = None
    category_name: Optional[str] = None
    description: Optional[str] = None

# --- Response Schema ---
class CategoryResponse(BaseModel):
    category_id: int
    exam_id: int
    category_name: str
    description: Optional[str]

    class Config:
        orm_mode = True
