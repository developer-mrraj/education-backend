
# app/routers/user_statistics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.test_session_answer import TestSessionAnswer
from app.models.user_statistics import UserStatistics
from app.models.test_sessions import TestSession
from app.schemas.user_statistics import (
    SessionStatisticsResponse,
    UserStatisticsResponse,
    UserStatisticsCreate,
    UserStatisticsUpdate
)

router = APIRouter(
    prefix="/user-statistics",
    tags=["User Statistics"]
)

# -------------------- CREATE USER STATISTICS --------------------
@router.post("/", response_model=UserStatisticsResponse)
def create_user_statistics(data: UserStatisticsCreate, db: Session = Depends(get_db)):
    existing_stats = db.query(UserStatistics).filter(UserStatistics.user_id == data.user_id).first()
    if existing_stats:
        raise HTTPException(status_code=400, detail="Statistics for this user already exist")

    stats = UserStatistics(user_id=data.user_id)
    db.add(stats)
    db.commit()
    db.refresh(stats)
    return stats

# -------------------- GET ALL USER STATISTICS --------------------
@router.get("/", response_model=List[UserStatisticsResponse])
def get_all_user_statistics(db: Session = Depends(get_db)):
    stats_list = db.query(UserStatistics).all()
    return stats_list

# -------------------- GET USER STATISTICS BY USER ID --------------------
@router.get("/{user_id}", response_model=UserStatisticsResponse)
def get_user_statistics(user_id: int, db: Session = Depends(get_db)):
    stats = db.query(UserStatistics).filter(UserStatistics.user_id == user_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="Statistics not found for this user")
    return stats

# -------------------- UPDATE USER STATISTICS --------------------
@router.put("/{user_id}", response_model=UserStatisticsResponse)
def update_user_statistics(
    user_id: int,
    data: UserStatisticsUpdate,
    db: Session = Depends(get_db)
):
    stats = db.query(UserStatistics).filter(UserStatistics.user_id == user_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="Statistics not found for this user")

    # Update values if provided
    if data.total_tests_attempted is not None:
        stats.total_tests_attempted = data.total_tests_attempted
    if data.total_questions_practiced is not None:
        stats.total_questions_practiced = data.total_questions_practiced
    if data.best_score is not None:
        stats.best_score = data.best_score
    if data.last_test_date is not None:
        stats.last_test_date = data.last_test_date
    else:
        stats.last_test_date = datetime.utcnow()

    # Automatically calculate accuracy
    if stats.total_questions_practiced > 0:
        # Calculate total correct from all test sessions of this user
        total_correct = db.query(TestSession).filter(TestSession.user_id == user_id).with_entities(
            func.sum(TestSession.correct)
        ).scalar() or 0
        stats.accuracy = (total_correct / stats.total_questions_practiced) * 100
    else:
        stats.accuracy = 0.0

    db.commit()
    db.refresh(stats)
    return stats

# -------------------- DELETE USER STATISTICS --------------------
@router.delete("/{user_id}")
def delete_user_statistics(user_id: int, db: Session = Depends(get_db)):
    stats = db.query(UserStatistics).filter(UserStatistics.user_id == user_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="Statistics not found for this user")
    
    db.delete(stats)
    db.commit()
    return {"detail": "User statistics deleted successfully"}


# -------------------- GET SESSION STATISTICS --------------------
@router.get("/session/{session_id}", response_model=SessionStatisticsResponse)
def get_session_statistics(session_id: int, db: Session = Depends(get_db)):
    session_answers = db.query(TestSessionAnswer).filter(
        TestSessionAnswer.session_id == session_id
    ).all()

    if not session_answers:
        raise HTTPException(status_code=404, detail="No answers found for this session")

    user_id = session_answers[0].user_id
    total_correct = sum(1 for ans in session_answers if ans.is_correct)
    total_attempted = sum(1 for ans in session_answers if ans.user_answer is not None)
    total_wrong = total_attempted - total_correct
    total_unattempted = len(session_answers) - total_attempted
    average_time = sum(ans.time_taken for ans in session_answers if ans.time_taken is not None) / total_attempted if total_attempted > 0 else 0.0
    accuracy = (total_correct / total_attempted) * 100 if total_attempted > 0 else 0.0

    return SessionStatisticsResponse(
        session_id=session_id,
        user_id=user_id,
        total_correct=total_correct,
        total_wrong=total_wrong,
        total_unattempted=total_unattempted,
        average_time=average_time,
        accuracy=accuracy
    )