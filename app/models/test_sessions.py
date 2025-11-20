# # app/models/test_sessions.py
# from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Boolean
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.core.database import Base

# class TestSession(Base):
#     __tablename__ = "test_sessions"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     test_series_id = Column(Integer, ForeignKey("test_series_list.id"), nullable=False)

#     started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     completed_at = Column(DateTime, nullable=True)

    
#  # relationships
#     answers = relationship("TestSessionAnswer", back_populates="session", cascade="all, delete-orphan")
#     user = relationship("User")
#     test_series = relationship("TestSeriesList")


from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class TestSession(Base):
    __tablename__ = "test_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    test_series_id = Column(Integer, ForeignKey("test_series_list.id"), nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # relationships
    answers = relationship("TestSessionAnswer", back_populates="session", cascade="all, delete-orphan")
    user = relationship("User", back_populates="test_sessions")
    test_series = relationship("TestSeriesList", back_populates="test_sessions")
