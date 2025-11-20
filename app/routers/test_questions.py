from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.core.database import get_db
from app.models.test_questions import TestQuestion
from app.models.test_summary import TestSummary
from app.schemas.test_questions import (
    TestQuestionCreate,
    TestQuestionUpdate,
    TestQuestionResponse
)

router = APIRouter(prefix="/questions", tags=["Test Questions"])

# # ------------------------------
# #  CREATE QUESTION (AUTO TRACK LATEST SUMMARY)
# # ------------------------------
# @router.post("/", response_model=TestQuestionResponse)
# def create_question(data: TestQuestionCreate, db: Session = Depends(get_db)):

#     # Step 1 → Auto-fetch the latest Test Summary
#     latest_summary = db.query(TestSummary).order_by(TestSummary.id.desc()).first()
#     if not latest_summary:
#         raise HTTPException(400, "No Test Summary found. Create a summary first.")

#     summary_id = latest_summary.id

#     # Step 2 → Create question with auto test_summary_id
#     question = TestQuestion(
#         test_summary_id=summary_id,
#         question_text=data.question_text,
#         option_a=data.option_a,
#         option_b=data.option_b,
#         option_c=data.option_c,
#         option_d=data.option_d,
#         correct_option=data.correct_option,
#         explanation=data.explanation
#     )

#     db.add(question)
#     db.commit()
#     db.refresh(question)

#     # Step 3 → Update question count in that section
#     question_count = db.query(TestQuestion).filter(
#         TestQuestion.test_summary_id == summary_id
#     ).count()

#     latest_summary.questions = question_count

#     # Step 4 → Update TOTALS for all sections in same test_series
#     all_sections = db.query(TestSummary).filter(
#         TestSummary.test_series_id == latest_summary.test_series_id
#     ).all()

#     total_q = sum(sec.questions for sec in all_sections)
#     total_m = sum(sec.marks for sec in all_sections)
#     total_d = sum(sec.duration for sec in all_sections)

#     for sec in all_sections:
#         sec.total_questions = total_q
#         sec.total_marks = total_m
#         sec.total_duration = total_d

#     db.commit()

#     return question

# ------------------------------------------------------------
#  CREATE QUESTION BY test_summary_id (MANUAL ASSIGN)
# ------------------------------------------------------------
@router.post("/by-summary/{test_summary_id}", response_model=TestQuestionResponse)
def create_question_by_summary_id(
    test_summary_id: int, 
    data: TestQuestionCreate, 
    db: Session = Depends(get_db)
):

    # Step 1 → Validate summary exists
    summary = db.query(TestSummary).filter(TestSummary.id == test_summary_id).first()
    if not summary:
        raise HTTPException(404, "Test Summary ID not found")

    # Step 2 → Insert question manually linked to given summary
    question = TestQuestion(
        test_summary_id=test_summary_id,
        question_text=data.question_text,
        option_a=data.option_a,
        option_b=data.option_b,
        option_c=data.option_c,
        option_d=data.option_d,
        correct_option=data.correct_option,
        explanation=data.explanation
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    # Step 3 → Update question count for this summary
    question_count = db.query(TestQuestion).filter(
        TestQuestion.test_summary_id == test_summary_id
    ).count()

    summary.questions = question_count

    # Step 4 → Update TOTALS for all sections of this test_series
    all_sections = db.query(TestSummary).filter(
        TestSummary.test_series_id == summary.test_series_id
    ).all()

    total_q = sum(sec.questions for sec in all_sections)
    total_m = sum(sec.marks for sec in all_sections)
    total_d = sum(sec.duration for sec in all_sections)

    for sec in all_sections:
        sec.total_questions = total_q
        sec.total_marks = total_m
        sec.total_duration = total_d

    db.commit()

    return question


# ------------------------------
#  GET ALL QUESTIONS
# ------------------------------
@router.get("/", response_model=list[TestQuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(TestQuestion).all()


# ------------------------------
#  GET QUESTION BY ID
# ------------------------------
@router.get("/{question_id}", response_model=TestQuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# ------------------------------
#  UPDATE QUESTION
# ------------------------------
@router.put("/{question_id}", response_model=TestQuestionResponse)
def update_question(
    question_id: int, data: TestQuestionUpdate, db: Session = Depends(get_db)
):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question


# ------------------------------
#  DELETE QUESTION
# ------------------------------
@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}


# ----------------------------------------------------------------
#  LOAD 20 QUESTIONS PER SECTION FOR GIVEN TEST SERIES (MYSQL)
# ----------------------------------------------------------------
@router.get("/load-by-series/{test_series_id}")
def load_questions(test_series_id: int, db: Session = Depends(get_db)):

    # Step 1: Get all sections from test_summary
    sections = db.query(TestSummary).filter(
        TestSummary.test_series_id == test_series_id
    ).all()

    if not sections:
        raise HTTPException(status_code=404, detail="No sections found")

    response = []

    # Step 2: For each section load 20 questions
    for section in sections:

        questions = (
            db.query(TestQuestion)
            .filter(TestQuestion.test_summary_id == section.id)
            .order_by(func.rand())      # <-- IMPORTANT for MySQL
            .limit(20)
            .all()
        )

        response.append({
            "section_name": section.section_name,
            "questions": questions
        })

    return {"sections": response}
