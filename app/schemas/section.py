# app/schemas/section.py

from pydantic import BaseModel

# ---------- Base ----------
class SectionBase(BaseModel):
    name: str


# ---------- Create ----------
class SectionCreate(SectionBase):
    pass


# ---------- Update ----------
class SectionUpdate(BaseModel):
    name: str


# ---------- Response ----------
class SectionResponse(SectionBase):
    id: int

    class Config:
        orm_mode = True
