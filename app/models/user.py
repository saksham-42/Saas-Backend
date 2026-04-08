from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=True, default="member")

    organization_members = relationship("OrganizationMember", back_populates="user", foreign_keys="OrganizationMember.user_id", passive_deletes=True)
    refresh_tokens = relationship("RefreshToken", back_populates="user", passive_deletes=True)
    tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to", passive_deletes=True)