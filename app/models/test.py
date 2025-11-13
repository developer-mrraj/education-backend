from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Test(Base):
    __tablename__ = "test"
    
    test_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    test_name = Column(String(100), nullable=False)
    total_questions = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, default=0.0)
    is_free = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("Category", backref="tests")
