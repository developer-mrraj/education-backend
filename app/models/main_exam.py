# models/main_exam.py

from sqlalchemy import Column, Integer, String, Boolean, Text
from app.core.database import Base

class MainExam(Base):
    __tablename__ = "main_exam"   # <-- renamed as requested

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_tests = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_free = Column(Boolean, default=False)

   
   

    

   
    

    
