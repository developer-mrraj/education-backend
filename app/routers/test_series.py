from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.test_series import TestSeriesList
from app.schemas.test_series import (
    TestSeriesListCreate, TestSeriesListUpdate, TestSeriesListResponse
)

router = APIRouter(prefix="/test-series", tags=["Test Series List"])


@router.post("/", response_model=TestSeriesListResponse)
def create_test_series(data: TestSeriesListCreate, db: Session = Depends(get_db)):
    series = TestSeriesList(**data.dict())
    db.add(series)
    db.commit()
    db.refresh(series)
    return series


@router.get("/", response_model=list[TestSeriesListResponse])
def get_all_series(db: Session = Depends(get_db)):
    return db.query(TestSeriesList).all()


@router.get("/{series_id}", response_model=TestSeriesListResponse)
def get_series(series_id: int, db: Session = Depends(get_db)):
    series = db.query(TestSeriesList).get(series_id)
    if not series:
        raise HTTPException(404, "Series not found")
    return series


@router.put("/{series_id}", response_model=TestSeriesListResponse)
def update_series(series_id: int, data: TestSeriesListUpdate, db: Session = Depends(get_db)):
    series = db.query(TestSeriesList).get(series_id)
    if not series:
        raise HTTPException(404, "Series not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(series, key, value)

    db.commit()
    db.refresh(series)
    return series


@router.delete("/{series_id}")
def delete_series(series_id: int, db: Session = Depends(get_db)):
    series = db.query(TestSeriesList).get(series_id)
    if not series:
        raise HTTPException(404, "Test series not found")

    db.delete(series)
    db.commit()
    return {"message": "Test series deleted successfully"}
