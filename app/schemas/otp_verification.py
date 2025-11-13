from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class OTPCreate(BaseModel):
    phone_no: str
    otp_code: str

class OTPVerify(BaseModel):
    phone_no: str
    otp_code: str

class OTPResponse(BaseModel):
    otp_id: int
    phone_no: str
    is_verified: bool
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True
