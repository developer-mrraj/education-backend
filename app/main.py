# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base, get_db

# Import routers
# from app.models import sections
from app.routers import otp_router, test_series_by_names,test_session_answer,user, user_statistics
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
from app.models.user import User
# from app.models.sections import Section


# Create FastAPI app instance
app = FastAPI()

# --- CORS Configuration ---
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:4200"
    # Add your frontend URL here
    # "https://yourfrontenddomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],         # Allow all HTTP methods
    allow_headers=["*"],         # Allow all headers
)



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
app.include_router(test_series_by_names.router)


# --- Auto-create tables at startup ---
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)  # This will create ALL tables

