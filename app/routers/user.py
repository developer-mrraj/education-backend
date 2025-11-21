from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.database import get_db
import app.models.user as user_models
import app.schemas.user as user_schemas
from app.utils.jwt_helper import create_access_token, verify_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -----------------------------
# PASSWORD HASHING
# -----------------------------
pwd_context = CryptContext(
    schemes=["argon2"],  # or "bcrypt" if argon2 not installed
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

# -----------------------------
# JWT AUTH
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

# -----------------------------
# CREATE USER (POST)
# -----------------------------
@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):

    existing = db.query(user_models.User).filter(
        (user_models.User.phone_no == user.phone_no) |
        (user_models.User.email == user.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    db_user = user_models.User(
        name=user.name,
        phone_no=user.phone_no,
        email=user.email,
        google_id=user.google_id,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(
        user_models.User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"user_id": user.user_id, "email": user.email},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------------
# GET ALL USERS (PROTECTED)
# -----------------------------
@router.get("/", response_model=List[user_schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(user_models.User).all()

# -----------------------------
# GET USER BY ID (PROTECTED)
# -----------------------------
@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(user_models.User).filter(
        user_models.User.user_id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# -----------------------------
# UPDATE USER (PROTECTED)
# -----------------------------
@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: int, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(user_models.User).filter(
        user_models.User.user_id == user_id
    ).first()

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
# DELETE USER (PROTECTED)
# -----------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(user_models.User).filter(
        user_models.User.user_id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

# -----------------------------
# Example Protected Route
# -----------------------------
@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}


