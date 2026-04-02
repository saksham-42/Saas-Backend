from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_database
from schemas import Org_create,Org_response,Task_create, Task_response
from auth.dependencies import get_user
from models.user import User
from models.organization import Organization
from models.organization_member import OrganizationMember
from models.task import Task

router = APIRouter(
    prefix= "/organization",
    tags= ["organization"]
)

@router.post("/", response_model=Org_response)
def create_organization(org: Org_create, db: Session = Depends(get_database), current_user : User = Depends(get_user)):
    existing = db.query(Organization).filter(Organization.slug == org.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")
    org = Organization(name=org.name, slug=org.slug, owner_id = current_user.id)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.get("/{org_id}", response_model=Org_response)
def get_organization(org_id: int, db: Session = Depends(get_database), current_user: User= Depends(get_user)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if current_user.org_id != org.id and org.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    return org

@router.post("/{curr_org_id}/members")
def add_members(curr_org_id : int, user_id: int,db: Session= Depends(get_database), curr_user: User = Depends(get_user)):
    org = db.query(Organization).filter(Organization.id==curr_org_id).first()
    if not org: 
        raise HTTPException(status_code=404, detail="Organization not found")
    if org.owner_id != curr_user.id:
        is_admin = db.query(OrganizationMember).filter(OrganizationMember.org_id==curr_user.id,OrganizationMember.user_id==user_id,OrganizationMember.role =="admin").first()
        if not is_admin:
            raise HTTPException(status_code=403, detail="Only admins can add members")
    existing = db.query(OrganizationMember).filter(OrganizationMember.user_id==user_id, OrganizationMember.org_id == curr_org_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="member already exists")
    member = OrganizationMember(org_id=curr_org_id, user_id=user_id, role = "member")
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{curr_org_id}/members")
def get_org(curr_org_id:int, db:Session=Depends(get_database),curr_user:User=Depends(get_user)):
    org = db.query(Organization).filter(Organization.id==curr_org_id).first()
    if not org:
        raise HTTPException(status_code=404,detail="Organization not found")
    is_member = db.query(OrganizationMember).filter(OrganizationMember.org_id==curr_org_id).first()
    if not is_member and org.owner_id!=curr_user.id:
        raise HTTPException(status_code=403, detail="Not a member of this organization")    
    members = db.query(OrganizationMember).filter(OrganizationMember.org_id==curr_org_id).all()
    return members

@router.post("/{org_id}/tasks", response_model=Task_response)
def create_tasks(org_id:int,task: Task_create ,curr_user: User = Depends(get_user), db:Session= Depends(get_database)):
    member = db.query(OrganizationMember).filter(OrganizationMember.org_id==org_id, OrganizationMember.user_id==curr_user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    new_task = Task(**task.model_dump(), org_id = org_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{org_id}/tasks", response_model=list[Task_response])
def get_tasks(org_id: int, curr_user: User = Depends(get_user), db: Session = Depends(get_database)):
    member = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id, OrganizationMember.user_id==curr_user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    return db.query(Task).filter(Task.org_id==org_id, Task.is_deleted==False).all()

