from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.schemas.organization import Org_create, Memb_role_update

def create_organization(org: Org_create, db: Session , current_user):
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

def add_members(org_id: int, db: Session, user_id: int, member):
    org = db.query(Organization).filter(Organization.id==org_id).first()
    if not org: 
        raise HTTPException(status_code=404, detail="Organization not found")
    if member.role !="admin":
        raise HTTPException(status_code=403, detail="Only admin can add members")
    existing = db.query(OrganizationMember).filter(OrganizationMember.org_id==org_id, OrganizationMember.user_id ==user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member already exists")
    memb = OrganizationMember(org_id = org_id, user_id = user_id, role = "member")
    db.add(memb)
    db.commit()
    db.refresh(memb)
    return memb

def get_members(db: Session, org_id: int, limit:int, skip:int):
    org_memb = db.query(OrganizationMember).filter(OrganizationMember.org_id==org_id).offset(skip).limit(limit).all()
    if not org_memb:
        raise HTTPException(status_code=404, detail="Wrong organization id")
    return org_memb

def get_organization(db: Session, org_id :int):
    org = db.query(Organization).filter(Organization.id==org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
    
def update_member_info(org_id: int, user_id: int, role: Memb_role_update, db: Session, member):
    if member.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins allowed to update details")
    org = db.query(Organization).filter(Organization.id==org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if org.owner_id == user_id:
        raise HTTPException(status_code=400, detail="Can't update the owner's role")
    memb = db.query(OrganizationMember).filter(OrganizationMember.org_id==org_id, OrganizationMember.user_id==user_id).first()
    if not memb:
        raise HTTPException(status_code=404, detail="Member not found")
    memb.role = role.role
    db.commit()
    db.refresh(memb)
    return memb

def remove_member(org_id: int, user_id: int, member, db: Session):
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

def remove_member(db: Session, org_id: int, user_id: int, member):
    if member.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can remove members")
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org.owner_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot remove the org owner")
    memb = db.query(OrganizationMember).filter(
        OrganizationMember.org_id == org_id,
        OrganizationMember.user_id == user_id
    ).first()
    if not memb:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(memb)
    db.commit()
    return {"message": "Member removed successfully!"}