# app/utils/sms_sender.py
# For demo, we just print OTP. Replace with real SMS API like Twilio
def send_sms(mobile_no: str, otp: str):
    print(f"Sending OTP {otp} to mobile number {mobile_no}")
    return True
