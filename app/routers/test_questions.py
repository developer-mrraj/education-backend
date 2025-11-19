# app/routers/test_questions.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.test_questions import TestQuestion
from app.models.sections import Section
from app.schemas.test_questions import (
    TestQuestionCreate,
    TestQuestionResponse,
    TestQuestionUpdate
)
from app.services.test_services import get_combined_questions_per_sections

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=TestQuestionResponse)
def create_question(payload: TestQuestionCreate, db: Session = Depends(get_db)):
    # Validate section exists
    section = db.query(Section).filter(Section.id == payload.section_id).first()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    q = TestQuestion(**payload.dict())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.get("/{question_id}", response_model=TestQuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.get("/test/{summary_id}", response_model=List[TestQuestionResponse])
def list_questions_for_test(summary_id: int, db: Session = Depends(get_db), limit: Optional[int] = Query(None, ge=1, le=1000)):
    query = db.query(TestQuestion).filter(TestQuestion.test_summary_id == summary_id)
    if limit:
        query = query.limit(limit)
    return query.all()


@router.delete("/{question_id}", status_code=204)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
    return None


@router.get("/fetch_per_section", response_model=List[TestQuestionResponse])
def fetch_questions_per_section(
    summary_id: int,
    section_ids: str = Query(..., description="Comma separated section ids in desired order, e.g. 1,2,3,4"),
    per_section: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Fetch `per_section` questions for each section id (in the order provided).
    Example: /questions/fetch_per_section?summary_id=7&section_ids=1,2,3,4&per_section=20
    """
    # parse section ids
    try:
        section_id_list = [int(s.strip()) for s in section_ids.split(",") if s.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_ids parameter")

    # Optional: validate all section ids exist
    existing = db.query(Section.id).filter(Section.id.in_(section_id_list)).all()
    existing_ids = {row.id for row in existing}
    missing = [sid for sid in section_id_list if sid not in existing_ids]
    if missing:
        raise HTTPException(status_code=400, detail=f"Sections not found: {missing}")

    questions = get_combined_questions_per_sections(db, summary_id, section_id_list, per_section)
    return questions
