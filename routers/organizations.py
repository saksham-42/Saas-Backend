from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_database
from schemas import Org_create,Org_response,Task_create, Task_response
from auth.dependencies import get_user, get_org_member
from models.user import User
from models.organization import Organization
from models.organization_member import OrganizationMember
from models.task import Task

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
    existing = db.query(OrganizationMember).filter(OrganizationMember.user_id==user_id, OrganizationMember.org_id == org_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member already exists")
    member = OrganizationMember(org_id=org_id, user_id=user_id, role = "member")
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{curr_org_id}/members")
def get_org(curr_org_id:int, db:Session=Depends(get_database),member:OrganizationMember = Depends(get_org_member)):   
    members = db.query(OrganizationMember).filter(OrganizationMember.org_id==curr_org_id).all()
    return members

@router.post("/{org_id}/tasks", response_model=Task_response)
def create_tasks(org_id:int,task: Task_create ,curr_user: User = Depends(get_org_member), db:Session= Depends(get_database)):
    new_task = Task(**task.model_dump(), org_id = org_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{org_id}/tasks", response_model=list[Task_response])
def get_tasks(org_id: int, curr_user: User = Depends(get_org_member), db: Session = Depends(get_database)):
    return db.query(Task).filter(Task.org_id==org_id, Task.is_deleted==False).all()

