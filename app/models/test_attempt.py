from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TestAttempt(Base):
    __tablename__ = "test_attempt"
    
    attempt_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    test_id = Column(Integer, ForeignKey("test.test_id"), nullable=False)
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    score = Column(Integer, nullable=True)
    status = Column(String(20), default="in_progress")  # in_progress, completed
    
    user = relationship("User", backref="test_attempts")
    test = relationship("Test", backref="attempts")
