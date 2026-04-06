from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

try:
    with engine.connect() as connection:
        print("Database connected successfully")
except Exception as e:
    print(f"Data base connection failed:{e}")
