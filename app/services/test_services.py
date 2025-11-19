# app/services/test_service.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from app.models.test_questions import TestQuestion

def get_questions_for_section(db: Session, summary_id: int, section_id: int, limit: int = 20) -> List[TestQuestion]:
    """
    Return up to `limit` questions for given test_summary_id and section_id in random order.
    """
    return (
        db.query(TestQuestion)
        .filter(
            TestQuestion.test_summary_id == summary_id,
            TestQuestion.section_id == section_id
        )
        .order_by(func.random())
        .limit(limit)
        .all()
    )

def get_combined_questions_per_sections(db: Session, summary_id: int, section_ids: List[int], per_section: int = 20) -> List[TestQuestion]:
    """
    Fetch `per_section` questions for each section_id in order of provided section_ids.
    Returns a flattened list where sections appear in the same order as section_ids.
    """
    questions = []
    for sid in section_ids:
        qlist = get_questions_for_section(db, summary_id, sid, per_section)
        questions.extend(qlist)
    return questions
