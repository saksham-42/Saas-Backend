from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    hashed_password = Column(String, nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable= True)

    organization = relationship("Organization", back_populates="users")