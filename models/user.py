from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    
    role = Column(String, nullable= False, index= True, default="member")
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    hashed_password = Column(String, nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable= True)

    organization = relationship("Organization", back_populates="users", foreign_keys=[org_id])
    organization_members = relationship("OrganizationMembers", back_populates="user", foreign_keys="OrganizationMember.user_id")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
