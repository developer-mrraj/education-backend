from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.category as category_models
import app.schemas.category as category_schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# CREATE CATEGORY
@router.post("/", response_model=category_schemas.CategoryResponse)
def create_category(category: category_schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = category_models.Category(
        exam_id=category.exam_id,
        category_name=category.category_name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# GET ALL CATEGORIES
@router.get("/", response_model=List[category_schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(category_models.Category).all()

# GET CATEGORY BY ID
@router.get("/{category_id}", response_model=category_schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(category_models.Category).filter(category_models.Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# UPDATE CATEGORY
@router.put("/{category_id}", response_model=category_schemas.CategoryResponse)
def update_category(category_id: int, category_update: category_schemas.CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(category_models.Category).filter(category_models.Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category_update.category_name:
        category.category_name = category_update.category_name
    if category_update.description:
        category.description = category_update.description
    if category_update.exam_id:
        category.exam_id = category_update.exam_id
    db.commit()
    db.refresh(category)
    return category

# DELETE CATEGORY
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(category_models.Category).filter(category_models.Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": f"Category with id {category_id} deleted successfully"}
