# app/models/test_session_answers.py
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class TestSessionAnswer(Base):
    __tablename__ = "test_session_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("test_questions.id", ondelete="CASCADE"), nullable=False)

    user_answer = Column(String(1), nullable=False)  # 'A'|'B'|'C'|'D'
    is_correct = Column(Boolean, nullable=False, default=False)
  

    # relationships
    session = relationship("TestSession", back_populates="answers")
    question = relationship("TestQuestion")
