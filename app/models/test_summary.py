from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class TestSummary(Base):
    __tablename__ = "test_summary"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key from test_series_list
    test_series_id = Column(Integer, ForeignKey("test_series_list.id", ondelete="CASCADE"), nullable=False)

    section_name = Column(String(100), nullable=False)
    questions = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    total_duration = Column(Integer, nullable=False)

    # Relationship if needed
    test_series = relationship("TestSeriesList", back_populates="summaries")
    test_questions = relationship("TestQuestion", back_populates="summary", cascade="all, delete")
