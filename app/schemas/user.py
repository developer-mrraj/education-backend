from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ----------------------
# Request Schema (for creating/updating user)
# ----------------------
class UserCreate(BaseModel):
    name: str
    phone_no: str
    email: Optional[EmailStr] = None
    google_id: Optional[str] = None
    password: str  # plain password; will be hashed in backend

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[EmailStr] = None

# ----------------------
# Response Schema (for API response)
# ----------------------
class UserResponse(BaseModel):
    user_id: int
    name: str
    phone_no: str
    email: Optional[EmailStr]
    google_id: Optional[str]
    created_at: datetime
    is_active: int

    class Config:
        orm_mode = True  # Important for SQLAlchemy ORM
