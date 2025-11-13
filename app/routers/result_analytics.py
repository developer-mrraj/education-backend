from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.result_analytics as result_models
import app.schemas.result_analytics as result_schemas

router = APIRouter(
    prefix="/results",
    tags=["Result Analytics"]
)

# CREATE RESULT
@router.post("/", response_model=result_schemas.ResultAnalyticsResponse)
def create_result(result: result_schemas.ResultAnalyticsCreate, db: Session = Depends(get_db)):
    db_result = result_models.ResultAnalytics(
        attempt_id=result.attempt_id,
        total_questions=result.total_questions,
        total_correct=result.total_correct,
        total_wrong=result.total_wrong,
        total_unattempted=result.total_unattempted,
        accuracy=result.accuracy,
        percentage=result.percentage
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


# GET RESULT BY ID
@router.get("/{result_id}", response_model=result_schemas.ResultAnalyticsResponse)
def get_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(result_models.ResultAnalytics).filter(result_models.ResultAnalytics.result_id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result

# UPDATE RESULT
@router.put("/{result_id}", response_model=result_schemas.ResultAnalyticsResponse)
def update_result(result_id: int, result_update: result_schemas.ResultAnalyticsUpdate, db: Session = Depends(get_db)):
    result = db.query(result_models.ResultAnalytics).filter(result_models.ResultAnalytics.result_id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    for field, value in result_update.dict(exclude_unset=True).items():
        setattr(result, field, value)
    db.commit()
    db.refresh(result)
    return result

# DELETE RESULT
@router.delete("/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(result_models.ResultAnalytics).filter(result_models.ResultAnalytics.result_id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"detail": f"Result with id {result_id} deleted successfully"}
