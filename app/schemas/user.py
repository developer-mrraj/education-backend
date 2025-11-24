from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ----------------------
# Create User Schema
# ----------------------
class UserCreate(BaseModel):
    name: str
    phone_no: str
    email: Optional[EmailStr] = None
    password: str  # plain password

# ----------------------
# Update User Schema
# ----------------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[EmailStr] = None

# ----------------------
# Login Schema
# ----------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----------------------
# User Response Schema
# ----------------------
class UserResponse(BaseModel):
    user_id: int
    name: str
    phone_no: str
    email: Optional[EmailStr]
    password: str
    created_at: datetime
    is_active: int

    class Config:
        orm_mode = True