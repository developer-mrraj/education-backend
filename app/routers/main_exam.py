from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.main_exam import MainExam
from app.schemas.main_exam import MainExamCreate, MainExamUpdate, MainExamResponse

router = APIRouter(prefix="/main-exam", tags=["Main Exam"])


@router.post("/", response_model=MainExamResponse)
def create_main_exam(data: MainExamCreate, db: Session = Depends(get_db)):
    exam = MainExam(**data.dict())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("/", response_model=list[MainExamResponse])
def get_all_main_exams(db: Session = Depends(get_db)):
    return db.query(MainExam).all()


@router.get("/{exam_id}", response_model=MainExamResponse)
def get_main_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(MainExam).get(exam_id)
    if not exam:
        raise HTTPException(404, "Main exam not found")
    return exam


@router.put("/{exam_id}", response_model=MainExamResponse)
def update_main_exam(exam_id: int, data: MainExamUpdate, db: Session = Depends(get_db)):
    exam = db.query(MainExam).get(exam_id)
    if not exam:
        raise HTTPException(404, "Main exam not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(exam, key, value)

    db.commit()
    db.refresh(exam)
    return exam


@router.delete("/{exam_id}")
def delete_main_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(MainExam).get(exam_id)
    if not exam:
        raise HTTPException(404, "Main exam not found")

    db.delete(exam)
    db.commit()
    return {"message": "Main exam deleted successfully"}
