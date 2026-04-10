from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import Task_create,TaskAssign,TaskStatus,TaskUpdate
from app.models.organization_member import OrganizationMember
from datetime import datetime, timezone
from typing import Optional

def create_tasks(org_id:int, task: Task_create, db:Session):
    if task.assigned_to:
        assignee = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id, OrganizationMember.user_id==task.assigned_to).first()
        if not assignee:
            raise HTTPException(status_code=400, detail="Assigned user isn't a part of organization")
    new_task = Task(**task.model_dump(), org_id = org_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session ,org_id: int,status: Optional[TaskStatus], skip : int , limit: int):
    task = db.query(Task).filter(Task.org_id==org_id, Task.is_deleted==False)
    if status:
        task = task.filter(Task.status==status)
    return task.offset(skip).limit(limit).all()

def update_task(org_id: int, task_id: int, task_update: TaskUpdate, db: Session ):
    task = db.query(Task).filter(Task.id == task_id, Task.org_id == org_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task

def assign_task(org_id:int, task_id: int, task_assign: TaskAssign, db : Session ):
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

def delete_task(org_id: int, task_id: int, db: Session):
    task = db.query(Task).filter(Task.id==task_id, Task.org_id==org_id, Task.is_deleted==False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_deleted =True
    task.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return {"message": "Task deleted!"}
