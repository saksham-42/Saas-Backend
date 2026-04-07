from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime, timezone

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, index= True, primary_key=True)
    name = Column(String, unique= True, nullable=False)
    slug = Column(String, unique= True, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True), nullable= False, default= lambda:datetime.now(timezone.utc))

    members = relationship("OrganizationMember", back_populates="organization", foreign_keys="OrganizationMember.org_id")
    tasks = relationship("Task", back_populates="organization", foreign_keys="Task.org_id")

