# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Dict, Any
# from pydantic import BaseModel

# from app.core.database import get_db
# from app.models.main_exam import MainExam
# from app.models.sub_exams import SubExam
# from app.models.test_series import TestSeriesList
# from app.models.test_summary import TestSummary
# from app.models.test_questions import TestQuestion
# from app.schemas.test_questions import TestQuestionCreate


# router = APIRouter(prefix="/Exam-Flow", tags=["Exam Flow"])


# # -------------------- Request Models --------------------
# class SectionWithQuestions(BaseModel):
#     section_name: str
#     questions: int
#     marks: int
#     duration: int
#     question_list: List[TestQuestionCreate]


# class CreateFullTestRequest(BaseModel):
#     main_exam_name: str
#     sub_exam_name: str
#     test_series: Dict[str, Any]
#     sections: List[SectionWithQuestions]


# # -------------------- COMBINED API --------------------
# @router.post("/create-full-test", response_model=dict)
# def create_full_test(
#     body: CreateFullTestRequest,
#     db: Session = Depends(get_db)
# ):

#     # 1️⃣ Validate Main Exam
#     main_exam = db.query(MainExam).filter(MainExam.title.ilike(body.main_exam_name)).first()
#     if not main_exam:
#         raise HTTPException(status_code=404, detail="Main Exam not found")

#     # 2️⃣ Validate Sub Exam
#     sub_exam = (
#         db.query(SubExam)
#         .filter(
#             SubExam.title.ilike(body.sub_exam_name),
#             SubExam.main_exam_id == main_exam.id
#         )
#         .first()
#     )
#     if not sub_exam:
#         raise HTTPException(status_code=404, detail="Sub Exam not found for the given Main Exam")

#     # 3️⃣ Create Test Series
#     series = body.test_series
#     new_series = TestSeriesList(
#         sub_exam_id=sub_exam.id,
#         series_number=series.get("series_number"),
#         title=series.get("title"),
#         duration_minutes=series.get("duration_minutes"),
#         total_questions=series.get("total_questions"),
#         is_active=series.get("is_active", True)
#     )
#     db.add(new_series)
#     db.commit()
#     db.refresh(new_series)

#     summary_records = []
#     question_records = []

#     total_q = total_m = total_d = 0

#     # 4️⃣ Create Test Summaries + Questions
#     for section in body.sections:
#         total_q += section.questions
#         total_m += section.marks
#         total_d += section.duration

#         new_summary = TestSummary(
#             test_series_id=new_series.id,
#             section_name=section.section_name,
#             questions=section.questions,
#             marks=section.marks,
#             duration=section.duration,
#             total_questions=total_q,
#             total_marks=total_m,
#             total_duration=total_d
#         )
#         db.add(new_summary)
#         db.commit()
#         db.refresh(new_summary)
#         summary_records.append(new_summary)

#         for q in section.question_list:
#             new_question = TestQuestion(
#                 test_summary_id=new_summary.id,
#                 **q.dict()
#             )
#             db.add(new_question)
#             db.commit()
#             db.refresh(new_question)
#             question_records.append(new_question)

#     # 5️⃣ Final Response (with main_exam_id & sub_exam_id included)
#     return {
#         "message": "Test Series, Sections & Questions created successfully",
#         "main_exam_id": main_exam.id,
#         "sub_exam_id": sub_exam.id,
#         "test_series": {
#             "id": new_series.id,
#             "series_number": new_series.series_number,
#             "title": new_series.title,
#             "duration_minutes": new_series.duration_minutes,
#             "total_questions": new_series.total_questions,
#             "is_active": new_series.is_active
#         },
#         "summaries": [
#             {
#                 "id": s.id,
#                 "section_name": s.section_name,
#                 "questions": s.questions,
#                 "marks": s.marks,
#                 "duration": s.duration,
#                 "total_questions": s.total_questions,
#                 "total_marks": s.total_marks,
#                 "total_duration": s.total_duration
#             }
#             for s in summary_records
#         ],
#         "questions": [
#             {
#                 "id": q.id,
#                 "summary_id": q.test_summary_id,
#                 "question_text": q.question_text,
#                 "option_a": q.option_a,
#                 "option_b": q.option_b,
#                 "option_c": q.option_c,
#                 "option_d": q.option_d,
#                 "correct_option": q.correct_option,
#                 "explanation": q.explanation
#             }
#             for q in question_records
#         ]
#     }


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.main_exam import MainExam
from app.models.sub_exams import SubExam
from app.models.test_series import TestSeriesList
from app.models.test_summary import TestSummary
from app.models.test_questions import TestQuestion
from app.schemas.test_questions import TestQuestionCreate

router = APIRouter(prefix="/Exam-Flow", tags=["Exam Flow"])

# -------------------- Request Models --------------------
class TestSeriesCreate(BaseModel):
    series_number: int
    title: str
    duration_minutes: int
    total_questions: int
    is_active: bool = True

class SectionWithQuestions(BaseModel):
    section_name: str
    questions: int
    marks: int
    duration: int
    question_list: List[TestQuestionCreate]

class CreateFullTestRequest(BaseModel):
    main_exam_id: int
    sub_exam_id: int
    test_series: TestSeriesCreate
    sections: List[SectionWithQuestions]

# -------------------- API: Create Full Test --------------------
@router.post("/create-full-test", response_model=dict)
def create_full_test(
    body: CreateFullTestRequest,
    db: Session = Depends(get_db)
):

    # 1️⃣ Validate Main Exam
    main_exam = db.query(MainExam).filter(MainExam.id == body.main_exam_id).first()
    if not main_exam:
        raise HTTPException(status_code=404, detail="Main Exam not found")

    # 2️⃣ Validate Sub Exam
    sub_exam = db.query(SubExam).filter(
        SubExam.id == body.sub_exam_id,
        SubExam.main_exam_id == main_exam.id
    ).first()
    if not sub_exam:
        raise HTTPException(status_code=404, detail="Sub Exam not found for the given Main Exam")

    # 3️⃣ Create Test Series
    ts = body.test_series
    new_series = TestSeriesList(
        sub_exam_id=sub_exam.id,  # Taken directly from body.sub_exam_id
        series_number=ts.series_number,
        title=ts.title,
        duration_minutes=ts.duration_minutes,
        total_questions=ts.total_questions,
        is_active=ts.is_active
    )
    db.add(new_series)
    db.commit()
    db.refresh(new_series)

    summary_records = []
    question_records = []

    total_q = total_m = total_d = 0

    # 4️⃣ Create Test Summaries + Questions
    for section in body.sections:
        total_q += section.questions
        total_m += section.marks
        total_d += section.duration

        new_summary = TestSummary(
            test_series_id=new_series.id,
            section_name=section.section_name,
            questions=section.questions,
            marks=section.marks,
            duration=section.duration,
            total_questions=total_q,
            total_marks=total_m,
            total_duration=total_d
        )
        db.add(new_summary)
        db.commit()
        db.refresh(new_summary)
        summary_records.append(new_summary)

        for q in section.question_list:
            new_question = TestQuestion(
                test_summary_id=new_summary.id,
                **q.dict()
            )
            db.add(new_question)
            db.commit()
            db.refresh(new_question)
            question_records.append(new_question)

    # 5️⃣ Final Response
    return {
        "message": "Test Series, Sections & Questions created successfully",
        "main_exam_id": main_exam.id,
        "sub_exam_id": sub_exam.id,
        "test_series": {
            "id": new_series.id,
            "series_number": new_series.series_number,
            "title": new_series.title,
            "duration_minutes": new_series.duration_minutes,
            "total_questions": new_series.total_questions,
            "is_active": new_series.is_active
        },
        "summaries": [
            {
                "id": s.id,
                "section_name": s.section_name,
                "questions": s.questions,
                "marks": s.marks,
                "duration": s.duration,
                "total_questions": s.total_questions,
                "total_marks": s.total_marks,
                "total_duration": s.total_duration
            }
            for s in summary_records
        ],
        "questions": [
            {
                "id": q.id,
                "summary_id": q.test_summary_id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_option": q.correct_option,
                "explanation": q.explanation
            }
            for q in question_records
        ]
    }
