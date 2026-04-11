from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
from app.core.logging import logger
import traceback

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
        logger.info("Database connected successfully")
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    logger.error(f"Full traceback:\n{traceback.format_exc()}")
    raise