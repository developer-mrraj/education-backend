from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.test_attempt as attempt_models
import app.schemas.test_attempt as attempt_schemas

router = APIRouter(
    prefix="/test_attempts",
    tags=["Test Attempts"]
)

# CREATE TEST ATTEMPT
@router.post("/", response_model=attempt_schemas.TestAttemptResponse)
def create_attempt(attempt: attempt_schemas.TestAttemptCreate, db: Session = Depends(get_db)):
    db_attempt = attempt_models.TestAttempt(
        user_id=attempt.user_id,
        test_id=attempt.test_id,
        start_time=attempt.start_time,
        end_time=attempt.end_time,
        score=attempt.score,
        status=attempt.status
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt



# GET ATTEMPT BY ID
@router.get("/{attempt_id}", response_model=attempt_schemas.TestAttemptResponse)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.query(attempt_models.TestAttempt).filter(attempt_models.TestAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt

# UPDATE ATTEMPT
@router.put("/{attempt_id}", response_model=attempt_schemas.TestAttemptResponse)
def update_attempt(attempt_id: int, attempt_update: attempt_schemas.TestAttemptUpdate, db: Session = Depends(get_db)):
    attempt = db.query(attempt_models.TestAttempt).filter(attempt_models.TestAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    for field, value in attempt_update.dict(exclude_unset=True).items():
        setattr(attempt, field, value)
    db.commit()
    db.refresh(attempt)
    return attempt

# DELETE ATTEMPT
@router.delete("/{attempt_id}")
def delete_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.query(attempt_models.TestAttempt).filter(attempt_models.TestAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    db.delete(attempt)
    db.commit()
    return {"detail": f"Attempt with id {attempt_id} deleted successfully"}
