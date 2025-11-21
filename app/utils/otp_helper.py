# app/utils/otp_helper.py
import random
from datetime import datetime, timedelta

def generate_otp(length=6):
    """Generate a numeric OTP"""
    otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

def otp_expiry_seconds(minutes=1):
    """Return expiry time in seconds for cache"""
    return minutes * 60
