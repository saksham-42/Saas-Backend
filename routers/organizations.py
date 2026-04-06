from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_database
from schemas import Org_create,Org_response
from auth.dependencies import get_user, get_org_member
from models.organization import Organization
from models.organization_member import OrganizationMember

router = APIRouter(
    prefix= "/organization",
    tags= ["organization"]
)

@router.post("/", response_model=Org_response)
def create_organization(org: Org_create, db: Session = Depends(get_database), current_user : OrganizationMember=Depends(get_user)):
    existing = db.query(Organization).filter(Organization.slug == org.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")
    org = Organization(name=org.name, slug=org.slug, owner_id = current_user.id)
    db.add(org)
    db.commit()
    db.refresh(org)
    member = OrganizationMember(org_id = org.id, user_id = current_user.id, role="admin")
    db.add(member)
    db.commit()
    return org

@router.get("/{org_id}", response_model=Org_response)
def get_organization(org_id: int, db: Session = Depends(get_database), member: OrganizationMember= Depends(get_org_member)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.post("/{org_id}/members")
def add_members(org_id : int, user_id: int,db: Session= Depends(get_database), member: OrganizationMember = Depends(get_org_member)):
    org = db.query(Organization).filter(Organization.id==org_id).first()
    if member.role !="admin":
        raise HTTPException(status_code=403, detail="Only admins can add members")
    if org.owner_id == user_id:
        raise HTTPException(status_code=400, detail="Owner is already an admin of this organization")
    existing = db.query(OrganizationMember).filter(OrganizationMember.user_id==user_id, OrganizationMember.org_id == org_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member already exists")
    member = OrganizationMember(org_id=org_id, user_id=user_id, role = "member")
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{org_id}/members")
def get_org(org_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_database), member: OrganizationMember = Depends(get_org_member)):
    members = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id).offset(skip).limit(limit).all()
    return members

@router.delete("/{org_id}/members/{user_id}", status_code=200)
def remove_member(org_id: int, user_id: int, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    if member.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can remove members")
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org.owner_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot remove the org owner")
    memb = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id,OrganizationMember.user_id == user_id).first()
    if not memb:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(memb)
    db.commit()
    return {"message": "Member removed successfully!"}
