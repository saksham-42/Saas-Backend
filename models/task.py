from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey
from db import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda:datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    organization = relationship("Organization",back_populates="tasks" ,foreign_keys=[org_id])
    assignee = relationship("User",back_populates="tasks" ,foreign_keys=[assigned_to])
    