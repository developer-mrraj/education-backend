# # app/routers/test_sessions.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime

# from app.core.database import get_db
# from app.models.test_sessions import TestSession
# from app.schemas.test_sessions import (
#     TestSessionCreate,
#     TestSessionEnd,
#     TestSessionResponse
# )

# router = APIRouter(prefix="/test-sessions", tags=["Test Sessions"])


# # ---------------------------------------------------
# # START TEST SESSION
# # ---------------------------------------------------
# @router.post("/", response_model=TestSessionResponse)
# def start_session(payload: TestSessionCreate, db: Session = Depends(get_db)):

#     session = TestSession(
#         user_id=payload.user_id,
#         test_series_id=payload.test_series_id,
#         # started_at auto from model
#     )

#     db.add(session)
#     db.commit()
#     db.refresh(session)

#     return session


# # ---------------------------------------------------
# # END TEST SESSION
# # ---------------------------------------------------
# @router.put("/{session_id}/end", response_model=TestSessionResponse)
# def end_session(session_id: int, db: Session = Depends(get_db)):

#     session = db.query(TestSession).filter(TestSession.id == session_id).first()

#     if not session:
#         raise HTTPException(404, "Session not found")

#     session.completed_at = datetime.utcnow()

#     db.commit()
#     db.refresh(session)

#     return session


# # ---------------------------------------------------
# # GET SINGLE SESSION
# # ---------------------------------------------------
# @router.get("/{session_id}", response_model=TestSessionResponse)
# def get_session(session_id: int, db: Session = Depends(get_db)):
#     session = db.query(TestSession).filter(TestSession.id == session_id).first()
#     if not session:
#         raise HTTPException(404, "Session not found")
#     return session


# # ---------------------------------------------------
# # GET ALL SESSIONS
# # ---------------------------------------------------
# @router.get("/", response_model=list[TestSessionResponse])
# def get_all_sessions(db: Session = Depends(get_db)):
#     return db.query(TestSession).all()


# # ---------------------------------------------------
# # DELETE SESSION
# # ---------------------------------------------------
# @router.delete("/{session_id}")
# def delete_session(session_id: int, db: Session = Depends(get_db)):
#     session = db.query(TestSession).filter(TestSession.id == session_id).first()

#     if not session:
#         raise HTTPException(404, "Session not found")

#     db.delete(session)
#     db.commit()

#     return {"message": "Session deleted successfully"}


# app/routers/test_sessions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.test_series import TestSeriesList
from app.models.test_sessions import TestSession
from app.models.user import User
from app.schemas.test_sessions import (
    TestSessionCreate,
    TestSessionEnd,
    TestSessionResponse
)

router = APIRouter(prefix="/test-sessions", tags=["Test Sessions"])

@router.post("/", response_model=TestSessionResponse)
def start_session(db: Session = Depends(get_db)):

    # Auto-pick LATEST user (optional logic)
    latest_user = (
        db.query(User)
        .order_by(User.user_id.desc())   # 🔥 FIXED HERE
        .first()
    )

    if not latest_user:
        raise HTTPException(400, "No user available")

    # Auto-pick latest test series
    latest_series = (
        db.query(TestSeriesList)
        .order_by(TestSeriesList.id.desc())
        .first()
    )

    if not latest_series:
        raise HTTPException(400, "No test series exists. Create a test series first.")

    session = TestSession(
        user_id=latest_user.user_id,      # 🔥 FIXED HERE
        test_series_id=latest_series.id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# ---------------------------------------------------
# END TEST SESSION
# ---------------------------------------------------
@router.put("/{session_id}/end", response_model=TestSessionResponse)
def end_session(session_id: int, db: Session = Depends(get_db)):

    session = db.query(TestSession).filter(TestSession.id == session_id).first()

    if not session:
        raise HTTPException(404, "Session not found")

    session.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(session)

    return session


# ---------------------------------------------------
# GET SINGLE SESSION
# ---------------------------------------------------
@router.get("/{session_id}", response_model=TestSessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(404, "Session not found")
    return session


# ---------------------------------------------------
# GET ALL SESSIONS
# ---------------------------------------------------
@router.get("/", response_model=list[TestSessionResponse])
def get_all_sessions(db: Session = Depends(get_db)):
    return db.query(TestSession).all()


# ---------------------------------------------------
# DELETE SESSION
# ---------------------------------------------------
@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.id == session_id).first()

    if not session:
        raise HTTPException(404, "Session not found")

    db.delete(session)
    db.commit()

    return {"message": "Session deleted successfully"}