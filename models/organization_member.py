from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class OrganizationMember(Base):
    __tablename__ = "organization_members"

    id = Column(Integer, index= True, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable= False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    role = Column(String, nullable=False, default="member")

    user = relationship("User", back_populates="organization_members",foreign_keys=[user_id])
    organization = relationship("Organization", back_populates="members",foreign_keys=[org_id])
    
