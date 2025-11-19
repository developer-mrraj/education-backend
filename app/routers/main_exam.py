# app/routers/main_exam.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.main_exam import MainExam
from app.schemas.main_exam import (
    MainExamCreate,
    MainExamUpdate,
    MainExamResponse
)

router = APIRouter(prefix="/main-exam", tags=["Main Exam"])


# ----------------------------
# Create Main Exam
# ----------------------------
@router.post("/", response_model=MainExamResponse)
def create_main_exam(data: MainExamCreate, db: Session = Depends(get_db)):
    new_exam = MainExam(**data.dict())

    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return new_exam


# ----------------------------
# Get All Main Exams
# ----------------------------
@router.get("/", response_model=list[MainExamResponse])
def get_all_main_exams(db: Session = Depends(get_db)):
    exams = db.query(MainExam).all()
    return exams


# ----------------------------
# Get Single Main Exam by ID
# ----------------------------
@router.get("/{exam_id}", response_model=MainExamResponse)
def get_main_exam_by_id(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(MainExam).filter(MainExam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Main Exam not found")

    return exam


# ----------------------------
# Update Main Exam
# ----------------------------
@router.put("/{exam_id}", response_model=MainExamResponse)
def update_main_exam(exam_id: int, data: MainExamUpdate, db: Session = Depends(get_db)):
    exam = db.query(MainExam).filter(MainExam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Main Exam not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(exam, key, value)

    db.commit()
    db.refresh(exam)

    return exam


# ----------------------------
# Delete Main Exam
# ----------------------------
@router.delete("/{exam_id}")
def delete_main_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(MainExam).filter(MainExam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Main Exam not found")

    db.delete(exam)
    db.commit()

    return {"message": "Main Exam deleted successfully"}
