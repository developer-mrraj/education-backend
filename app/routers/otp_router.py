# app/routers/otp_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
import app.models.user as user_models
from app.utils.otp_helper import generate_otp, otp_expiry_seconds
from app.utils.sms_sender import send_sms
from app.utils.jwt_helper import create_access_token

router = APIRouter(prefix="/otp", tags=["OTP"])

# Replace Redis with in-memory cache
otp_cache = {}

@router.post("/send")
def send_otp_api(mobile_no: str, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.phone_no == mobile_no).first()
    if not user:
        raise HTTPException(status_code=404, detail="Mobile number not registered")

    otp_code = generate_otp()
    expiry_time = timedelta(minutes=5)

    # Store in memory
    otp_cache[mobile_no] = {"otp": otp_code, "expires_at": datetime.utcnow() + expiry_time}

    send_sms(mobile_no, otp_code)
    return {"detail": "OTP sent successfully"}

@router.post("/verify")
def verify_otp_api(mobile_no: str, otp: str, db: Session = Depends(get_db)):
    if mobile_no not in otp_cache:
        raise HTTPException(status_code=400, detail="OTP expired or not generated")

    entry = otp_cache[mobile_no]
    if entry["expires_at"] < datetime.utcnow():
        del otp_cache[mobile_no]
        raise HTTPException(status_code=400, detail="OTP expired")

    if entry["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP correct → delete from cache
    del otp_cache[mobile_no]

    user = db.query(user_models.User).filter(user_models.User.phone_no == mobile_no).first()
    access_token = create_access_token(
        data={"user_id": user.user_id, "email": user.email},
        expires_delta=timedelta(minutes=60)
    )

    return {"access_token": access_token, "token_type": "bearer"}


