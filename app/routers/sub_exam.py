from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sub_exams import SubExam
from app.schemas.sub_exams import SubExamCreate, SubExamUpdate, SubExamResponse

router = APIRouter(prefix="/sub-exam", tags=["Sub Exam"])


@router.post("/", response_model=SubExamResponse)
def create_sub_exam(data: SubExamCreate, db: Session = Depends(get_db)):
    exam = SubExam(**data.dict())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("/", response_model=list[SubExamResponse])
def get_all_sub_exams(db: Session = Depends(get_db)):
    return db.query(SubExam).all()


@router.get("/{sub_exam_id}", response_model=SubExamResponse)
def get_sub_exam(sub_exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(SubExam).get(sub_exam_id)
    if not exam:
        raise HTTPException(404, "Sub exam not found")
    return exam


@router.put("/{sub_exam_id}", response_model=SubExamResponse)
def update_sub_exam(sub_exam_id: int, data: SubExamUpdate, db: Session = Depends(get_db)):
    exam = db.query(SubExam).get(sub_exam_id)
    if not exam:
        raise HTTPException(404, "Sub exam not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(exam, key, value)

    db.commit()
    db.refresh(exam)
    return exam


@router.delete("/{sub_exam_id}")
def delete_sub_exam(sub_exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(SubExam).get(sub_exam_id)
    if not exam:
        raise HTTPException(404, "Sub exam not found")

    db.delete(exam)
    db.commit()
    return {"message": "Sub exam deleted successfully"}
