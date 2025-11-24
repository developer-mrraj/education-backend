# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# # ✅ Direct connection string for your local MySQL database
# DATABASE_URL = "mysql+pymysql://raj:password123@192.168.1.6:3306/geekbychoice"
DATABASE_URL = "mysql+pymysql://shareduser1:pass1234@192.168.1.4:3306/edudatabase"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,          # shows SQL logs in terminal (useful to confirm DB connection)
    pool_pre_ping=True
)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency function for FastAPI routes to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
