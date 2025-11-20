# models/sub_exam.py

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SubExam(Base):
    __tablename__ = "sub_exam"

    id = Column(Integer, primary_key=True, index=True)

    main_exam_id = Column(Integer, ForeignKey("main_exam.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(200), nullable=False)         # IBPS PO
    subtitle = Column(String(200), nullable=True)       # Probationary Officer
    # tagline = Column(String(200), nullable=True)        # IBPS PO Test Series

    total_tests = Column(Integer, nullable=False, default=0)  # 50 tests

   
    thumbnail_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)

    # Relationship (optional)
    main_exam = relationship("MainExam", backref="sub_exams")
