from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.test_questions import TestQuestion
from app.schemas.test_questions import (
    TestQuestionCreate, TestQuestionUpdate, TestQuestionResponse
)

router = APIRouter(prefix="/test-questions", tags=["Test Questions"])


@router.post("/", response_model=TestQuestionResponse)
def create_question(data: TestQuestionCreate, db: Session = Depends(get_db)):
    question = TestQuestion(**data.dict())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.get("/", response_model=list[TestQuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(TestQuestion).all()


@router.get("/{question_id}", response_model=TestQuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).get(question_id)
    if not question:
        raise HTTPException(404, "Question not found")
    return question


@router.put("/{question_id}", response_model=TestQuestionResponse)
def update_question(question_id: int, data: TestQuestionUpdate, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).get(question_id)
    if not question:
        raise HTTPException(404, "Question not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)
    return question


@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).get(question_id)
    if not question:
        raise HTTPException(404, "Question not found")

    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}
