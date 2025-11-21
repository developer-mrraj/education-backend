from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone_no = Column(String(15), unique=True, nullable=False)
    google_id = Column(String(100), unique=True, nullable=True)
    password = Column(String(256), nullable=False)  # hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Integer, default=1)  # Optional: for soft delete/block user
