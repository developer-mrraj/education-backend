# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from app.core.database import Base


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

#     correct_option = Column(String(1), nullable=False)   # A/B/C/D

#     explanation = Column(Text, nullable=True)

#     # Relationship back
#     summary = relationship("TestSummary", back_populates="test_questions")


# app/models/test_questions.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)

    test_summary_id = Column(
        Integer,
        ForeignKey("test_summary.id", ondelete="CASCADE"),
        nullable=False
    )

    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False
    )

    question_text = Column(Text, nullable=False)

    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)

    correct_option = Column(String(1), nullable=False)   # A/B/C/D

    explanation = Column(Text, nullable=True)

    # relationships (optional but helpful)
    summary = relationship("TestSummary", back_populates="test_questions")
    section = relationship("Section")
