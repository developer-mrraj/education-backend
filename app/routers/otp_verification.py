# app/routers/otp_verification.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import randint
from app.core.database import get_db
from app.models.otp_verification import OTPVerification
from datetime import datetime

router = APIRouter(prefix="/otp", tags=["OTP"])

# --- Send OTP ---
@router.post("/send")
def send_otp(phone_no: str, db: Session = Depends(get_db)):
    otp_code = randint(100000, 999999)  # generate 6-digit OTP
    otp_entry = OTPVerification(phone_no=phone_no, otp_code=str(otp_code), is_verified=False)
    db.add(otp_entry)
    db.commit()
    db.refresh(otp_entry)
    
    # Here you can integrate SMS sending service
    print(f"OTP for {phone_no}: {otp_code}")
    
    return {"message": "OTP sent successfully", "otp_id": otp_entry.otp_id}

# --- Verify OTP ---
@router.post("/verify")
def verify_otp(phone_no: str, otp_code: str, db: Session = Depends(get_db)):
    otp_entry = db.query(OTPVerification).filter(
        OTPVerification.phone_no == phone_no,
        OTPVerification.otp_code == otp_code
    ).first()
    
    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    otp_entry.is_verified = True
    db.commit()
    return {"message": "OTP verified successfully"}
