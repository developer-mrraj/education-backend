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

# -------------------- CREATE ANSWER FOR SPECIFIC SESSION & QUESTION --------------------
@router.post("/session/{session_id}/question/{question_id}", response_model=TestSessionAnswerResponse)
def create_answer_for_session_question(
    session_id: int,
    question_id: int,
    answer_data: TestSessionAnswerUpdate,   # only user_answer
    db: Session = Depends(get_db)
):
    # Validate session
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")

    # Validate question
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check duplicate
    existing_answer = db.query(TestSessionAnswer).filter(
        TestSessionAnswer.session_id == session_id,
        TestSessionAnswer.question_id == question_id
    ).first()
    if existing_answer:
        raise HTTPException(status_code=400, detail="Answer already submitted for this question")

    # Check correctness
    is_correct = (
        answer_data.user_answer.upper() == question.correct_option.upper()
        if hasattr(question, "correct_option") else False
    )

    # Create new answer
    new_answer = TestSessionAnswer(
        session_id=session_id,
        question_id=question_id,
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


@router.post("/submit/{session_id}")
def submit_all_answers(session_id: int, data: dict, db: Session = Depends(get_db)):
    answers = data.get("answers", [])

    # Validate session
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")

    for ans in answers:
        question_id = ans["question_id"]
        user_answer = ans["user_answer"].upper()

        # Validate question
        question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail=f"Question {question_id} not found")

        # Check existing answer (update if exists)
        existing = db.query(TestSessionAnswer).filter(
            TestSessionAnswer.session_id == session_id,
            TestSessionAnswer.question_id == question_id
        ).first()

        is_correct = (user_answer == question.correct_option.upper())

        if existing:
            # Update existing
            existing.user_answer = user_answer
            existing.is_correct = is_correct
        else:
            # Insert new answer
            new_answer = TestSessionAnswer(
                session_id=session_id,
                question_id=question_id,
                user_answer=user_answer,
                is_correct=is_correct
            )
            db.add(new_answer)

    db.commit()
    return {"detail": "All answers submitted successfully"}
