# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import engine, Base, get_db

# Import all models so SQLAlchemy knows them
import app.models.user as user_models
import app.models.exam as exam_models
import app.models.category as category_models
import app.models.test as test_models
import app.models.questions as question_models
import app.models.test_attempt as attempt_models
import app.models.attempt_answer as answer_models
import app.models.result_analytics as result_models
import app.models.payment as payment_models

# Import schemas
import app.schemas.user as user_schemas
import app.schemas.exam as exam_schemas
import app.schemas.category as category_schemas
import app.schemas.test as test_schemas
import app.schemas.question as question_schemas
import app.schemas.test_attempt as attempt_schemas
import app.schemas.attempt_answer as answer_schemas
import app.schemas.result_analytics as result_schemas
import app.schemas.payment as payment_schemas

# Import routers
from app.routers import otp_router, user
from app.routers import exam
from app.routers import category
from app.routers import test
from app.routers import questions
from app.routers import test_attempt
from app.routers import attempt_answer
from app.routers import result_analytics
from app.routers import payment


# Create FastAPI app instance
app = FastAPI()


app.include_router(user.router)
app.include_router(otp_router.router)
app.include_router(exam.router)
app.include_router(category.router)
app.include_router(test.router)
app.include_router(questions.router)
app.include_router(test_attempt.router)
app.include_router(attempt_answer.router)
app.include_router(result_analytics.router)
app.include_router(payment.router)

# --- Auto-create tables at startup ---
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)  # This will create ALL tables


