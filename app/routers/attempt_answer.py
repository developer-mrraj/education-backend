from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.attempt_answer as answer_models
import app.schemas.attempt_answer as answer_schemas
import app.models.questions as question_models

router = APIRouter(
    prefix="/attempt_answers",
    tags=["Attempt Answers"]
)

# # CREATE ATTEMPT ANSWER
# @router.post("/", response_model=answer_schemas.AttemptAnswerResponse)
# def create_answer(answer: answer_schemas.AttemptAnswerCreate, db: Session = Depends(get_db)):
#     db_answer = answer_models.AttemptAnswer(
#         attempt_id=answer.attempt_id,
#         question_id=answer.question_id,
#         selected_option=answer.selected_option,
#         is_correct=answer.is_correct
#     )
#     db.add(db_answer)
#     db.commit()
#     db.refresh(db_answer)
#     return db_answer

# --- Create Attempt Answer ---
@router.post("/", response_model=answer_schemas.AttemptAnswerResponse)
def create_answer(answer: answer_schemas.AttemptAnswerCreate, db: Session = Depends(get_db)):
    # Get the correct answer for the question
    question = db.query(question_models.Question).filter(question_models.Question.question_id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Compare the selected answer with correct answer
    is_correct = (answer.selected_option == question.correct_option)

    db_answer = answer_models.AttemptAnswer(
        attempt_id=answer.attempt_id,
        question_id=answer.question_id,
        selected_option=answer.selected_option,
        is_correct=is_correct
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

# GET ALL ANSWERS
@router.get("/", response_model=List[answer_schemas.AttemptAnswerResponse])
def get_answers(db: Session = Depends(get_db)):
    return db.query(answer_models.AttemptAnswer).all()

# GET ANSWER BY ID
@router.get("/{answer_id}", response_model=answer_schemas.AttemptAnswerResponse)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(answer_models.AttemptAnswer).filter(answer_models.AttemptAnswer.answer_id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

# UPDATE ANSWER
@router.put("/{answer_id}", response_model=answer_schemas.AttemptAnswerResponse)
def update_answer(answer_id: int, answer_update: answer_schemas.AttemptAnswerUpdate, db: Session = Depends(get_db)):
    answer = db.query(answer_models.AttemptAnswer).filter(answer_models.AttemptAnswer.answer_id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    for field, value in answer_update.dict(exclude_unset=True).items():
        setattr(answer, field, value)
    db.commit()
    db.refresh(answer)
    return answer

# DELETE ANSWER
@router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(answer_models.AttemptAnswer).filter(answer_models.AttemptAnswer.answer_id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(answer)
    db.commit()
    return {"detail": f"Answer with id {answer_id} deleted successfully"}
