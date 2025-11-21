# app/routers/test_series_by_names.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.models.main_exam import MainExam
from app.models.sub_exams import SubExam
from app.models.test_series import TestSeriesList
from app.schemas.test_series import TestSeriesListResponse

router = APIRouter(prefix="/test-series-by-names", tags=["Test Series By Names"])

# ---------------- Request Body Schema ----------------
class TestSeriesFetchRequest(BaseModel):
    main_exam_name: str
    sub_exam_name: str


# ---------------- Fetch Test Series ----------------
@router.post("/", response_model=List[TestSeriesListResponse])
def get_test_series_by_names(data: TestSeriesFetchRequest, db: Session = Depends(get_db)):
    # 1. Find Main Exam by name (case-insensitive)
    main_exam = db.query(MainExam).filter(MainExam.title.ilike(data.main_exam_name)).first()
    if not main_exam:
        raise HTTPException(status_code=404, detail="Main Exam not found")

    # 2. Find Sub Exam by name and parent Main Exam
    sub_exam = (
        db.query(SubExam)
        .filter(
            SubExam.title.ilike(data.sub_exam_name),
            SubExam.main_exam_id == main_exam.id
        )
        .first()
    )
    if not sub_exam:
        raise HTTPException(status_code=404, detail="Sub Exam not found for the given Main Exam")

    # 3. Fetch all Test Series for that Sub Exam
    test_series_list = db.query(TestSeriesList).filter(TestSeriesList.sub_exam_id == sub_exam.id).all()

    if not test_series_list:
        raise HTTPException(status_code=404, detail="No Test Series found for the given Sub Exam")

    return test_series_list
