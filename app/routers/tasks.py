from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.task import Task_create,Task_response,TaskAssign,TaskStatus,TaskUpdate
from app.auth.dependencies import get_org_member
from app.models.user import User
from app.models.organization_member import OrganizationMember
from app.core.db import get_database
from typing import Optional
import app.services.task_service as task_service

router = APIRouter(
    prefix = "/organization",
    tags = ["tasks"]
)

@router.post("/{org_id}/tasks", response_model=Task_response)
def create_tasks(org_id:int, task: Task_create ,member: OrganizationMember = Depends(get_org_member), db:Session= Depends(get_database)):
    return task_service.create_tasks(org_id, task, db)

@router.get("/{org_id}/tasks", response_model=list[Task_response])
def get_tasks(org_id: int,status: Optional[TaskStatus] = None, skip: int= 0, limit: int= 10, curr_user: User = Depends(get_org_member), db: Session = Depends(get_database)):
    return task_service.get_tasks(db, org_id, status,skip, limit)

@router.put("/{org_id}/tasks/{task_id}", response_model=Task_response)
def update_task(org_id: int, task_id: int, task_update: TaskUpdate, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    return task_service.update_task(org_id, task_id, task_update, db)

@router.patch("/{org_id}/tasks/{task_id}/assign", response_model=Task_response)
def assign_task(org_id:int, task_id: int, task_assign: TaskAssign, member: OrganizationMember = Depends(get_org_member), db : Session = Depends(get_database)):
    return task_service.assign_task(org_id, task_id, task_assign, db)

@router.delete("/{org_id}/tasks/{task_id}", status_code=200)
def delete_task(org_id: int, task_id: int, member: OrganizationMember = Depends(get_org_member), db: Session = Depends(get_database)):
    return task_service.delete_task(org_id, task_id, db)
