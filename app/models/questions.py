from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Question(Base):
    __tablename__ = "question"
    
    question_id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test.test_id"), nullable=False)
    question_text = Column(String(500), nullable=False)
    option_a = Column(String(200), nullable=False)
    option_b = Column(String(200), nullable=False)
    option_c = Column(String(200), nullable=False)
    option_d = Column(String(200), nullable=False)
    correct_option = Column(String(1), nullable=False)  # 'A','B','C','D'
    marks = Column(Integer, default=1)
    
    test = relationship("Test", backref="questions")
