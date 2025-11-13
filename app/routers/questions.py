from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.questions as question_models
import app.schemas.question as question_schemas

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

# CREATE QUESTION
@router.post("/", response_model=question_schemas.QuestionResponse)
def create_question(question: question_schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = question_models.Question(
        test_id=question.test_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_option=question.correct_option,
        marks=question.marks
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# GET ALL QUESTIONS
@router.get("/", response_model=List[question_schemas.QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    return db.query(question_models.Question).all()

# UPDATE QUESTION
@router.put("/{question_id}", response_model=question_schemas.QuestionResponse)
def update_question(question_id: int, question_update: question_schemas.QuestionUpdate, db: Session = Depends(get_db)):
    question = db.query(question_models.Question).filter(question_models.Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    for field, value in question_update.dict(exclude_unset=True).items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return question

# DELETE QUESTION
@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(question_models.Question).filter(question_models.Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"detail": f"Question with id {question_id} deleted successfully"}
