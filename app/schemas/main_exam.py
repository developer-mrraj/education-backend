# app/schemas/main_exam.py

from pydantic import BaseModel
from typing import Optional

class MainExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    total_tests: Optional[int] = 0
    price: Optional[int] = None
    thumbnail_url: Optional[str] = None
    is_active: Optional[bool] = True
    is_free: Optional[bool] = False


class MainExamCreate(MainExamBase):
    pass


class MainExamUpdate(MainExamBase):
    pass


class MainExamResponse(MainExamBase):
    id: int

    class Config:
        orm_mode = True
