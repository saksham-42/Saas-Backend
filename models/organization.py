from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, index= True, primary_key=True)
    name = Column(String, unique= True, nullable=False)
    slug = Column(String, unique= True, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime, nullable= False, default=datetime.utcnow)

    users = relationship("User", back_populates="organization")

