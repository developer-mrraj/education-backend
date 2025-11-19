from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# class TestQuestion(Base):
#     __tablename__ = "test_questions"

#     id = Column(Integer, primary_key=True, index=True)

#     test_summary_id = Column(
#         Integer,
#         ForeignKey("test_summary.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     question_text = Column(Text, nullable=False)

#     option_a = Column(String(255), nullable=False)
#     option_b = Column(String(255), nullable=False)
#     option_c = Column(String(255), nullable=False)
#     option_d = Column(String(255), nullable=False)

#     correct_option = Column(String(1), nullable=False)
#     explanation = Column(Text, nullable=True)

#     # # Relationship
#     # test_summary = relationship("TestSummary", back_populates="test_questions")
#     test_summary = relationship(
#     "TestSummary",
#     back_populates="test_questions"
# )

class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)
    test_summary_id = Column(
        Integer,
        ForeignKey("test_summary.id", ondelete="CASCADE"),
        nullable=False
    )
    question_text = Column(Text, nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    correct_option = Column(String(1), nullable=False)
    explanation = Column(Text, nullable=True)

    # Relationship with TestSummary
    test_summary = relationship("TestSummary", back_populates="test_questions")

    # Relationship with TestSessionAnswer (missing)
    answers = relationship("TestSessionAnswer", back_populates="question", cascade="all, delete")
