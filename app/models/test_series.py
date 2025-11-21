# models/test_series_list.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class TestSeriesList(Base):
    __tablename__ = "test_series_list"

    id = Column(Integer, primary_key=True, index=True)

    sub_exam_id = Column(Integer, ForeignKey("sub_exam.id", ondelete="CASCADE"), nullable=False)

    series_number = Column(Integer, nullable=False)         # 1
    title = Column(String(200), nullable=False)             # Test Series 1
    duration_minutes = Column(Integer, nullable=False)      # 60 mins
    total_questions = Column(Integer, nullable=False)       # 100 questions

    is_active = Column(Boolean, default=True)

    # Relationship
    sub_exam = relationship("SubExam", backref="test_series_list")
    summaries = relationship("TestSummary", back_populates="test_series", cascade="all, delete")
