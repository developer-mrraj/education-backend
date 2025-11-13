from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payment"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    test_id = Column(Integer, ForeignKey("test.test_id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String(20), nullable=False)  # success, failed, pending
    payment_mode = Column(String(50), nullable=False)   # upi, card, razorpay
    transaction_id = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="payments")
    test = relationship("Test", backref="payments")
