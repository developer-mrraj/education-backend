# app/models/section.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
