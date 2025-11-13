from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Exam(Base):
    __tablename__ = "exam"
    
    exam_id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String(100), nullable=False)
    description = Column(String(256), nullable=True)
    logo_url = Column(String(256), nullable=True)
    is_active = Column(Integer, default=1)  # Optional: hide inactive exams
