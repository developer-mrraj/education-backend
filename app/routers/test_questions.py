from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.core.database import get_db
from app.models.test_questions import TestQuestion
from app.models.test_summary import TestSummary
from app.schemas.test_questions import (
    TestQuestionCreate,
    TestQuestionUpdate,
    TestQuestionResponse
)

router = APIRouter(prefix="/questions", tags=["Test Questions"])


# ------------------------------
#  CREATE QUESTION
# ------------------------------
@router.post("/", response_model=TestQuestionResponse)
def create_question(data: TestQuestionCreate, db: Session = Depends(get_db)):
    question = TestQuestion(**data.dict())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


# ------------------------------
#  GET ALL QUESTIONS
# ------------------------------
@router.get("/", response_model=list[TestQuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(TestQuestion).all()


# ------------------------------
#  GET QUESTION BY ID
# ------------------------------
@router.get("/{question_id}", response_model=TestQuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# ------------------------------
#  UPDATE QUESTION
# ------------------------------
@router.put("/{question_id}", response_model=TestQuestionResponse)
def update_question(
    question_id: int, data: TestQuestionUpdate, db: Session = Depends(get_db)
):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question


# ------------------------------
#  DELETE QUESTION
# ------------------------------
@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}


# ----------------------------------------------------------------
#  LOAD 20 QUESTIONS PER SECTION FOR GIVEN TEST SERIES (MYSQL)
# ----------------------------------------------------------------
@router.get("/load-by-series/{test_series_id}")
def load_questions(test_series_id: int, db: Session = Depends(get_db)):

    # Step 1: Get all sections from test_summary
    sections = db.query(TestSummary).filter(
        TestSummary.test_series_id == test_series_id
    ).all()

    if not sections:
        raise HTTPException(status_code=404, detail="No sections found")

    response = []

    # Step 2: For each section load 20 questions
    for section in sections:

        questions = (
            db.query(TestQuestion)
            .filter(TestQuestion.test_summary_id == section.id)
            .order_by(func.rand())      # <-- IMPORTANT for MySQL
            .limit(20)
            .all()
        )

        response.append({
            "section_name": section.section_name,
            "questions": questions
        })

    return {"sections": response}
