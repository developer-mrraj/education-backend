# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.models.test_summary import TestSummary
# from app.schemas.test_summary import (
#     TestSummaryCreate, TestSummaryUpdate, TestSummaryResponse
# )

# router = APIRouter(prefix="/test-summary", tags=["Test Summary"])


# @router.post("/", response_model=TestSummaryResponse)
# def create_summary(data: TestSummaryCreate, db: Session = Depends(get_db)):
#     summary = TestSummary(**data.dict())
#     db.add(summary)
#     db.commit()
#     db.refresh(summary)
#     return summary


# @router.get("/", response_model=list[TestSummaryResponse])
# def get_all_summaries(db: Session = Depends(get_db)):
#     return db.query(TestSummary).all()


# @router.get("/{summary_id}", response_model=TestSummaryResponse)
# def get_summary(summary_id: int, db: Session = Depends(get_db)):
#     summary = db.query(TestSummary).get(summary_id)
#     if not summary:
#         raise HTTPException(404, "Summary not found")
#     return summary


# @router.put("/{summary_id}", response_model=TestSummaryResponse)
# def update_summary(summary_id: int, data: TestSummaryUpdate, db: Session = Depends(get_db)):
#     summary = db.query(TestSummary).get(summary_id)
#     if not summary:
#         raise HTTPException(404, "Summary not found")

#     for key, value in data.dict(exclude_unset=True).items():
#         setattr(summary, key, value)

#     db.commit()
#     db.refresh(summary)
#     return summary


# @router.delete("/{summary_id}")
# def delete_summary(summary_id: int, db: Session = Depends(get_db)):
#     summary = db.query(TestSummary).get(summary_id)
#     if not summary:
#         raise HTTPException(404, "Summary not found")

#     db.delete(summary)
#     db.commit()
#     return {"message": "Summary deleted successfully"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.models.test_summary import TestSummary
from app.schemas.test_summary import (
    TestSummaryCreate,
    TestSummaryUpdate,
    TestSummaryResponse
)

router = APIRouter(prefix="/test-summary", tags=["Test Summary"])


# -------------------------------
# CREATE SUMMARY (1 section)
# -------------------------------
@router.post("/", response_model=TestSummaryResponse)
def create_summary(data: TestSummaryCreate, db: Session = Depends(get_db)):
    
    # Calculate totals
    total_q = data.questions
    total_m = data.marks
    total_d = data.duration

    summary = TestSummary(
        test_series_id=data.test_series_id,
        section_name=data.section_name,
        questions=data.questions,
        marks=data.marks,
        duration=data.duration,

        total_questions=total_q,
        total_marks=total_m,
        total_duration=total_d
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


# -------------------------------
# GET ALL SUMMARIES
# -------------------------------
@router.get("/", response_model=list[TestSummaryResponse])
def get_all_summaries(db: Session = Depends(get_db)):
    return db.query(TestSummary).all()


# -------------------------------
# GET SINGLE SUMMARY
# -------------------------------
@router.get("/{summary_id}", response_model=TestSummaryResponse)
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(TestSummary).get(summary_id)
    if not summary:
        raise HTTPException(404, "Summary not found")
    return summary


# -------------------------------
# UPDATE SUMMARY (Recalculate totals)
# -------------------------------
@router.put("/{summary_id}", response_model=TestSummaryResponse)
def update_summary(summary_id: int, data: TestSummaryUpdate, db: Session = Depends(get_db)):
    summary = db.query(TestSummary).get(summary_id)
    if not summary:
        raise HTTPException(404, "Summary not found")

    # Update fields
    for key, value in data.dict(exclude_unset=True).items():
        setattr(summary, key, value)

    # Recalculate totals
    summary.total_questions = summary.questions
    summary.total_marks = summary.marks
    summary.total_duration = summary.duration

    db.commit()
    db.refresh(summary)
    return summary


# -------------------------------
# DELETE SUMMARY
# -------------------------------
@router.delete("/{summary_id}")
def delete_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(TestSummary).get(summary_id)
    if not summary:
        raise HTTPException(404, "Summary not found")

    db.delete(summary)
    db.commit()

    return {"message": "Summary deleted successfully"}
