from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.test as test_models
import app.schemas.test as test_schemas

router = APIRouter(
    prefix="/tests",
    tags=["Tests"]
)

# CREATE TEST
@router.post("/", response_model=test_schemas.TestResponse)
def create_test(test: test_schemas.TestCreate, db: Session = Depends(get_db)):
    db_test = test_models.Test(
        category_id=test.category_id,
        test_name=test.test_name,
        total_questions=test.total_questions,
        total_marks=test.total_marks,
        duration_minutes=test.duration_minutes,
        price=test.price,
        is_free=test.is_free
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

# GET ALL TESTS
@router.get("/", response_model=List[test_schemas.TestResponse])
def get_tests(db: Session = Depends(get_db)):
    return db.query(test_models.Test).all()

# GET TEST BY ID
@router.get("/{test_id}", response_model=test_schemas.TestResponse)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(test_models.Test).filter(test_models.Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

# UPDATE TEST
@router.put("/{test_id}", response_model=test_schemas.TestResponse)
def update_test(test_id: int, test_update: test_schemas.TestUpdate, db: Session = Depends(get_db)):
    test = db.query(test_models.Test).filter(test_models.Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    for field, value in test_update.dict(exclude_unset=True).items():
        setattr(test, field, value)
    db.commit()
    db.refresh(test)
    return test

# DELETE TEST
@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(test_models.Test).filter(test_models.Test.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(test)
    db.commit()
    return {"detail": f"Test with id {test_id} deleted successfully"}
