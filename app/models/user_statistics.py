# app/models/user_statistics.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class UserStatistics(Base):
    __tablename__ = "user_statistics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)

    total_tests_attempted = Column(Integer, default=0, nullable=False)
    total_questions_practiced = Column(Integer, default=0, nullable=False)
    best_score = Column(Float, default=0.0, nullable=False)
    accuracy = Column(Float, default=0.0, nullable=False)
    last_test_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="statistics")