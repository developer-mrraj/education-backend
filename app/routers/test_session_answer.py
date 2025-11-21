
# app/routers/test_session_answers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.test_session_answer import TestSessionAnswer
from app.models.test_sessions import TestSession
from app.models.test_questions import TestQuestion
from app.schemas.test_session_answers import (
    TestSessionAnswerCreate,
    TestSessionAnswerUpdate,
    TestSessionAnswerResponse
)

router = APIRouter(
    prefix="/test-session-answers",
    tags=["Test Session Answers"]
)

# -------------------- CREATE / ADD ANSWER --------------------
@router.post("/", response_model=TestSessionAnswerResponse)
def create_test_session_answer(answer_data: TestSessionAnswerCreate, db: Session = Depends(get_db)):
    # Validate session exists
    session = db.query(TestSession).filter(TestSession.id == answer_data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")
    
    # Validate question exists
    question = db.query(TestQuestion).filter(TestQuestion.id == answer_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if answer already exists for this session & question
    existing_answer = db.query(TestSessionAnswer).filter(
        TestSessionAnswer.session_id == answer_data.session_id,
        TestSessionAnswer.question_id == answer_data.question_id
    ).first()
    if existing_answer:
        raise HTTPException(status_code=400, detail="Answer for this question already submitted")

    # Check correctness
    is_correct = answer_data.user_answer.upper() == question.correct_option.upper() if hasattr(question, "correct_option") else False

    new_answer = TestSessionAnswer(
        session_id=answer_data.session_id,
        question_id=answer_data.question_id,
        user_answer=answer_data.user_answer.upper(),
        is_correct=is_correct
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

# -------------------- GET ALL ANSWERS --------------------
@router.get("/", response_model=List[TestSessionAnswerResponse])
def get_all_test_session_answers(db: Session = Depends(get_db)):
    answers = db.query(TestSessionAnswer).all()
    return answers

# -------------------- GET ANSWERS BY SESSION --------------------
@router.get("/session/{session_id}", response_model=List[TestSessionAnswerResponse])
def get_answers_by_session(session_id: int, db: Session = Depends(get_db)):
    answers = db.query(TestSessionAnswer).filter(TestSessionAnswer.session_id == session_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="No answers found for this session")
    return answers

# -------------------- UPDATE AN ANSWER --------------------
@router.put("/{answer_id}", response_model=TestSessionAnswerResponse)
def update_test_session_answer(answer_id: int, answer_data: TestSessionAnswerUpdate, db: Session = Depends(get_db)):
    answer = db.query(TestSessionAnswer).filter(TestSessionAnswer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    # Update the user_answer
    answer.user_answer = answer_data.user_answer.upper()
    
    # Recalculate correctness
    question = db.query(TestQuestion).filter(TestQuestion.id == answer.question_id).first()
    answer.is_correct = answer.user_answer.upper() == question.correct_option.upper() if hasattr(question, "correct_option") else False

    db.commit()
    db.refresh(answer)
    return answer

# -------------------- DELETE AN ANSWER --------------------
@router.delete("/{answer_id}")
def delete_test_session_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(TestSessionAnswer).filter(TestSessionAnswer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    db.delete(answer)
    db.commit()
    return {"detail": "Test session answer deleted successfully"}
