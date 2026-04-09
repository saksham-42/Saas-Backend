from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL , pool_size=10, max_overflow=20, pool_pre_ping=True)

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
