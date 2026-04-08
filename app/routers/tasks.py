from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import Task_create,Task_response,TaskAssign,TaskStatus,TaskUpdate
from app.auth.dependencies import get_org_member
from app.models.user import User
from app.models.organization_member import OrganizationMember
from app.core.db import get_database
from datetime import datetime, timezone
from typing import Optional

router = APIRouter(
    prefix = "/organization",
    tags = ["tasks"]
)

@router.post("/{org_id}/tasks", response_model=Task_response)
def create_tasks(org_id:int, task: Task_create ,member: OrganizationMember = Depends(get_org_member), db:Session= Depends(get_database)):
    if task.assigned_to:
        assignee = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id, OrganizationMember.user_id==task.assigned_to).first()
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
    return task

@router.delete("/{org_id}/tasks/{task_id}", status_code=200)
def delete_task(org_id: int, task_id: int, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id==task_id, Task.org_id==org_id, Task.is_deleted==False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_deleted =True
    task.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return {"message": "Task deleted!"}
