from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class OTPVerification(Base):
    __tablename__ = "otp_verification"
    
    otp_id = Column(Integer, primary_key=True, index=True)
    phone_no = Column(String(15), nullable=False)
    otp_code = Column(String(10), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Optional: OTP expiry
