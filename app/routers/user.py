from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.user as user_models
import app.schemas.user as user_schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -----------------------------
# CREATE USER (POST)
# -----------------------------
@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(user_models.User).filter(
        (user_models.User.phone_no == user.phone_no) | 
        (user.email != None and user_models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = user_models.User(
        name=user.name,
        phone_no=user.phone_no,
        email=user.email,
        google_id=user.google_id,
        password=user.password  # TODO: hash password in production
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -----------------------------
# GET ALL USERS (GET)
# -----------------------------
@router.get("/", response_model=List[user_schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(user_models.User).all()
    return users

# -----------------------------
# GET USER BY ID (GET)
# -----------------------------
@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -----------------------------
# UPDATE USER (PUT)
# -----------------------------
@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: int, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name:
        user.name = user_update.name
    if user_update.phone_no:
        user.phone_no = user_update.phone_no
    if user_update.email:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user

# -----------------------------
# DELETE USER (DELETE)
# -----------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"User with id {user_id} deleted successfully"}
