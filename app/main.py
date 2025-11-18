# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import engine, Base, get_db

# Import routers
from app.routers import otp_router, test_session_answer,user, user_statistics
from app.routers import main_exam
from app.routers import sub_exam
from app.routers import test_series
from app.routers import test_summary
from app.routers import test_questions
from app.routers import test_sessions 

# Import new models so tables are created
from app.models.test_sessions import TestSession
from app.models.test_session_answer import TestSessionAnswer
from app.models.user_statistics import UserStatistics


# Create FastAPI app instance
app = FastAPI()


app.include_router(user.router)
app.include_router(otp_router.router)
app.include_router(main_exam.router)
app.include_router(sub_exam.router)
app.include_router(test_series.router)
app.include_router(test_summary.router)
app.include_router(test_questions.router)
# Include your new TestSession router
app.include_router(test_sessions.router)
app.include_router(test_session_answer.router)
app.include_router(user_statistics.router)

# --- Auto-create tables at startup ---
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)  # This will create ALL tables

