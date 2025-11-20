from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.main_exam import MainExam
from app.models.sub_exams import SubExam
from app.schemas.sub_exams import SubExamCreate, SubExamUpdate, SubExamResponse

router = APIRouter(prefix="/sub-exam", tags=["Sub Exam"])


# # ---------------- CREATE using latest main exam ----------------
# @router.post("/", response_model=SubExamResponse)
# def create_sub_exam(data: SubExamCreate, db: Session = Depends(get_db)):
#     latest_main_exam = db.query(MainExam).order_by(MainExam.id.desc()).first()
#     if not latest_main_exam:
#         raise HTTPException(status_code=400, detail="No main exam found to link this sub-exam")

#     exam = SubExam(
#         main_exam_id=latest_main_exam.id,
#         title=data.title,
#         subtitle=data.subtitle,
#         total_tests=data.total_tests,
#         thumbnail_url=data.thumbnail_url,
#         is_active=data.is_active
#     )
#     db.add(exam)
#     db.commit()
#     db.refresh(exam)
#     return exam


# ---------------- CREATE using specific main_exam_id ----------------
@router.post("/by-main/{main_exam_id}", response_model=SubExamResponse)
def create_sub_exam_by_main_id(main_exam_id: int, data: SubExamCreate, db: Session = Depends(get_db)):

    # Check if main exam exists
    main_exam = db.query(MainExam).filter(MainExam.id == main_exam_id).first()
    if not main_exam:
        raise HTTPException(status_code=404, detail="Main exam not found")

    exam = SubExam(
        main_exam_id=main_exam_id,
        title=data.title,
        subtitle=data.subtitle,
        total_tests=data.total_tests,
        thumbnail_url=data.thumbnail_url,
        is_active=data.is_active
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


# ---------------- GET all ----------------
@router.get("/", response_model=list[SubExamResponse])
def get_all_sub_exams(db: Session = Depends(get_db)):
    return db.query(SubExam).all()


# ---------------- GET single ----------------
@router.get("/{sub_exam_id}", response_model=SubExamResponse)
def get_sub_exam(sub_exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(SubExam).get(sub_exam_id)
    if not exam:
        raise HTTPException(404, "Sub exam not found")
    return exam


# ---------------- UPDATE ----------------
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


# ---------------- DELETE ----------------
@router.delete("/{sub_exam_id}")
def delete_sub_exam(sub_exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(SubExam).get(sub_exam_id)
    if not exam:
        raise HTTPException(404, "Sub exam not found")

    db.delete(exam)
    db.commit()
    return {"message": "Sub exam deleted successfully"}
