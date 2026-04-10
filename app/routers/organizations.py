from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_database
from app.schemas.organization import Org_create,Org_response, Memb_role_update
from app.auth.dependencies import get_user, get_org_member
from app.models.organization_member import OrganizationMember
from app.models.user import User
import app.services.org_service as org_service

router = APIRouter(
    prefix= "/organization",
    tags= ["organization"]
)

@router.post("/", response_model=Org_response)
def create_organization(org: Org_create, db: Session = Depends(get_database), current_user : User = Depends(get_user)):
    return org_service.create_organization(org, db, current_user)

@router.get("/{org_id}", response_model=Org_response)
def get_organization(org_id: int, db: Session = Depends(get_database), member: OrganizationMember = Depends(get_org_member)):
    return org_service.get_organization(db, org_id)

@router.post("/{org_id}/members")
def add_members(org_id : int, user_id: int,db: Session= Depends(get_database), member: OrganizationMember = Depends(get_org_member)):
    return org_service.add_members(org_id, db, user_id, member)

@router.get("/{org_id}/members")
def get_members(org_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_database), member: OrganizationMember = Depends(get_org_member)):
    return org_service.get_members(db, org_id, limit, skip)

@router.patch("/{org_id}/members/{user_id}/role")
def update_member_info(org_id: int, user_id: int, role: Memb_role_update, db: Session = Depends(get_database), member: OrganizationMember = Depends(get_org_member)):
    return org_service.update_member_info(org_id, user_id, role, db, member)

@router.delete("/{org_id}/members/{user_id}", status_code=200)
def remove_member(org_id: int, user_id: int, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    return org_service.remove_member(db,org_id, user_id, member)
