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


# ----------------------------------------------------
# CREATE SUMMARY (Fix: calculate totals BEFORE commit)
# ----------------------------------------------------
@router.post("/", response_model=TestSummaryResponse)
def create_summary(data: TestSummaryCreate, db: Session = Depends(get_db)):

    # STEP 1 → Fetch existing sections for this test series
    existing_sections = db.query(TestSummary).filter(
        TestSummary.test_series_id == data.test_series_id
    ).all()

    # STEP 2 → Calculate totals INCLUDING the new section
    total_q = sum(s.questions for s in existing_sections) + data.questions
    total_m = sum(s.marks for s in existing_sections) + data.marks
    total_d = sum(s.duration for s in existing_sections) + data.duration

    # STEP 3 → Insert NEW SECTION with pre-filled totals
    new_section = TestSummary(
        test_series_id=data.test_series_id,
        section_name=data.section_name,
        questions=data.questions,
        marks=data.marks,
        duration=data.duration,
        total_questions=total_q,
        total_marks=total_m,
        total_duration=total_d,
    )
    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    # STEP 4 → Update TOTALS in ALL rows
    all_sections = db.query(TestSummary).filter(
        TestSummary.test_series_id == data.test_series_id
    ).all()

    for sec in all_sections:
        sec.total_questions = total_q
        sec.total_marks = total_m
        sec.total_duration = total_d

    db.commit()
    db.refresh(new_section)

    return new_section


# ----------------------------------------------------
# GET ALL SUMMARIES
# ----------------------------------------------------
@router.get("/", response_model=list[TestSummaryResponse])
def get_all_summaries(db: Session = Depends(get_db)):
    return db.query(TestSummary).all()


# ----------------------------------------------------
# GET SINGLE SUMMARY
# ----------------------------------------------------
@router.get("/{summary_id}", response_model=TestSummaryResponse)
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(TestSummary).get(summary_id)
    if not summary:
        raise HTTPException(404, "Summary not found")
    return summary


# ----------------------------------------------------
# UPDATE SUMMARY (Recalculate totals)
# ----------------------------------------------------
@router.put("/{summary_id}", response_model=TestSummaryResponse)
def update_summary(summary_id: int, data: TestSummaryUpdate, db: Session = Depends(get_db)):
    summary = db.query(TestSummary).get(summary_id)
    if not summary:
        raise HTTPException(404, "Summary not found")

    # Update fields
    for key, value in data.dict(exclude_unset=True).items():
        setattr(summary, key, value)

    # Recalculate totals for this test_series_id
    all_sections = db.query(TestSummary).filter(
        TestSummary.test_series_id == summary.test_series_id
    ).all()

    total_q = sum(s.questions for s in all_sections)
    total_m = sum(s.marks for s in all_sections)
    total_d = sum(s.duration for s in all_sections)

    # update for all
    for sec in all_sections:
        sec.total_questions = total_q
        sec.total_marks = total_m
        sec.total_duration = total_d

    db.commit()
    db.refresh(summary)
    return summary


# ----------------------------------------------------
# DELETE SUMMARY
# ----------------------------------------------------
@router.delete("/{summary_id}")
def delete_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(TestSummary).get(summary_id)
    if not summary:
        raise HTTPException(404, "Summary not found")

    db.delete(summary)
    db.commit()

    return {"message": "Summary deleted successfully"}
