# test_db_connection.py
from .database import engine

try:
    with engine.connect() as connection:
        print("✅ Successfully connected to MySQL database 'geekbychoice'")
except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)
