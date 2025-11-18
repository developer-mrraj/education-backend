# app/routers/test_sessions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.test_sessions import TestSession
from app.schemas.test_sessions import TestSessionCreate, TestSessionEnd, TestSessionResponse

router = APIRouter(
    prefix="/test-sessions",
    tags=["Test Sessions"]
)

# -------------------- CREATE / START A TEST SESSION --------------------
@router.post("/", response_model=TestSessionResponse)
def create_test_session(session_data: TestSessionCreate, db: Session = Depends(get_db)):
    new_session = TestSession(
        user_id=session_data.user_id,
        test_series_id=session_data.test_series_id,
        total_questions=session_data.total_questions
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# -------------------- GET ALL TEST SESSIONS --------------------
@router.get("/", response_model=List[TestSessionResponse])
def get_all_test_sessions(db: Session = Depends(get_db)):
    sessions = db.query(TestSession).all()
    return sessions

# -------------------- GET A SINGLE TEST SESSION BY ID --------------------
@router.get("/{session_id}", response_model=TestSessionResponse)
def get_test_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")
    return session

# -------------------- UPDATE / END A TEST SESSION --------------------
@router.put("/{session_id}", response_model=TestSessionResponse)
def end_test_session(session_id: int, session_end: TestSessionEnd, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")
    
    session.attempted = session_end.attempted
    session.correct = session_end.correct
    session.wrong = session_end.wrong
    session.score = session_end.score
    session.completed_at = session_end.completed_at or datetime.utcnow()
    
    # calculate accuracy
    if session.attempted > 0:
        session.accuracy = (session.correct / session.attempted) * 100
    else:
        session.accuracy = 0.0

    db.commit()
    db.refresh(session)
    return session

# -------------------- DELETE A TEST SESSION --------------------
@router.delete("/{session_id}")
def delete_test_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test session not found")
    
    db.delete(session)
    db.commit()
    return {"detail": "Test session deleted successfully"}
