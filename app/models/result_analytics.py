from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ResultAnalytics(Base):
    __tablename__ = "result_analytics"
    
    result_id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("test_attempt.attempt_id"), nullable=False)
    total_questions = Column(Integer, nullable=False)
    total_correct = Column(Integer, nullable=False)
    total_wrong = Column(Integer, nullable=False)
    total_unattempted = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    attempt = relationship("TestAttempt", backref="result")
