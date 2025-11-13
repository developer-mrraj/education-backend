from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "category"
    
    category_id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exam.exam_id"), nullable=False)
    category_name = Column(String(100), nullable=False)
    description = Column(String(256), nullable=True)
    
    exam = relationship("Exam", backref="categories")
