from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.exam as exam_models
import app.schemas.exam as exam_schemas

router = APIRouter(
    prefix="/exams",
    tags=["Exams"]
)

# CREATE EXAM
@router.post("/", response_model=exam_schemas.ExamResponse)
def create_exam(exam: exam_schemas.ExamCreate, db: Session = Depends(get_db)):
    db_exam = exam_models.Exam(
        exam_name=exam.exam_name,
        description=exam.description,
        logo_url=exam.logo_url
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

# GET ALL EXAMS
@router.get("/", response_model=List[exam_schemas.ExamResponse])
def get_exams(db: Session = Depends(get_db)):
    return db.query(exam_models.Exam).all()

# GET EXAM BY ID
@router.get("/{exam_id}", response_model=exam_schemas.ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(exam_models.Exam).filter(exam_models.Exam.exam_id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

# UPDATE EXAM
@router.put("/{exam_id}", response_model=exam_schemas.ExamResponse)
def update_exam(exam_id: int, exam_update: exam_schemas.ExamUpdate, db: Session = Depends(get_db)):
    exam = db.query(exam_models.Exam).filter(exam_models.Exam.exam_id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    if exam_update.exam_name:
        exam.exam_name = exam_update.exam_name
    if exam_update.description:
        exam.description = exam_update.description
    if exam_update.logo_url:
        exam.logo_url = exam_update.logo_url
    db.commit()
    db.refresh(exam)
    return exam

# DELETE EXAM
@router.delete("/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(exam_models.Exam).filter(exam_models.Exam.exam_id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    db.delete(exam)
    db.commit()
    return {"detail": f"Exam with id {exam_id} deleted successfully"}
