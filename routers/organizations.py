from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_database
from schemas import Org_create,Org_response,Task_create, Task_response, TaskStatus, TaskUpdate, TaskAssign
from auth.dependencies import get_user, get_org_member
from models.user import User
from models.organization import Organization
from models.organization_member import OrganizationMember
from models.task import Task
from datetime import datetime, timezone
from typing import Optional

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

@router.post("/{org_id}/tasks", response_model=Task_response)
def create_tasks(org_id:int,task: Task_create ,curr_user: User = Depends(get_org_member), db:Session= Depends(get_database)):
    if task.assigned_to:
        assignee = db.query(OrganizationMember).filter(OrganizationMember.id == org_id, OrganizationMember.user_id==task.assigned_to).first()
        if not assignee:
            raise HTTPException(status_code=400, detail="Assigned user isn't a part of organization")
    new_task = Task(**task.model_dump(), org_id = org_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{org_id}/tasks", response_model=list[Task_response])
def get_tasks(org_id: int,status: Optional[TaskStatus] = None, skip: int= 0, limit: int= 10, curr_user: User = Depends(get_org_member), db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.org_id==org_id, Task.is_deleted==False)
    if status:
        task = task.filter(Task.status==status)
    return task.offset(skip).limit(limit).all()

@router.put("/{org_id}/tasks/{task_id}", response_model=Task_response)
def update_task(org_id: int, task_id: int, task_update: TaskUpdate, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id == task_id, Task.org_id == org_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{org_id}/tasks/{task_id}/assign", response_model=Task_response)
def assign_task(org_id:int, task_id: int, task_assign: TaskAssign, member: OrganizationMember = Depends(get_org_member), db : Session = Depends(get_database)):
    assignee = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id, OrganizationMember.user_id == task_assign.assigned_to).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found in organization")
    task = db.query(Task).filter(Task.id == task_id, Task.org_id==org_id, Task.is_deleted==False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assigned_to = task_assign.assigned_to
    db.commit()
    db.refresh(task)
    return task;

@router.delete("/{org_id}/tasks/{task_id}", status_code=200)
def delete_task(org_id: int, task_id: int, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id==task_id, Task.org_id==org_id, Task.is_deleted==False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_deleted =True
    task.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return {"message": "Task deleted!"}
