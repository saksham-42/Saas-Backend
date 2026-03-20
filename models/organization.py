from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, index= True, primary_key=True)
    name = Column(String, unique= True, nullable=False) 

    users = relationship("User", back_populates="organization")

