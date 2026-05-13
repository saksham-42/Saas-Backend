from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import Task_create, TaskAssign, TaskStatus, TaskUpdate, Task_response
from app.models.organization_member import OrganizationMember
from app.core.websocket_manager import manager
from app.core.cache import cache_delete_pattern, cache_get, cache_set
from datetime import datetime, timezone
from typing import Optional

TASKS_CACHE = 60

def _tasks_cache_key(org_id: int, skip: int, limit: int) -> str:
    return f"tasks:org:{org_id}:skip:{skip}:limit:{limit}"

def create_tasks(org_id: int, task: Task_create, db: Session):
    "Create a new task in an organization. Raises 400 if the assignee is not an org member."
    if task.assigned_to:
        assignee = db.query(OrganizationMember).filter(
            OrganizationMember.org_id == org_id,
            OrganizationMember.user_id == task.assigned_to).first()
        if not assignee:
            raise HTTPException(status_code=400, detail="Assigned user isn't a part of organization")
    new_task = Task(**task.model_dump(), org_id=org_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    cache_delete_pattern(f"tasks:org:{org_id}:*") 
    return new_task


def get_tasks(db: Session, org_id: int, status: Optional[TaskStatus], skip: int, limit: int, search : Optional[str] = None):
    "Return paginated non-deleted tasks for an org, optionally filtered by status."
    cache_key = _tasks_cache_key(org_id, skip, limit)
    cached = cache_get(cache_key)
    if cached is not None:
        return cached
    tasks = db.query(Task).filter(Task.org_id == org_id, Task.is_deleted.is_(False))
    if status:
        tasks = tasks.filter(Task.status == status)
    if search:
        tasks = tasks.filter(
            text("to_tsvector('english', coalesce(tasks.title, '') || ' ' || coalesce(tasks.description, '')) @@ plainto_tsquery('english', :search)")
        ).params(search=search)
    result = tasks.offset(skip).limit(limit).all()
    cache_set(cache_key, [Task_response.model_validate(t).model_dump() for t in result], ttl=TASKS_CACHE)
    return result


def update_task(org_id: int, task_id: int, task_update: TaskUpdate, db: Session):
    "Update a task's status. Raises 404 if task not found or already deleted."
    task = db.query(Task).filter(Task.id == task_id, Task.org_id == org_id, Task.is_deleted.is_(False)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    cache_delete_pattern(f"tasks:org:{org_id}:*")
    manager.broadcast_sync(org_id, {
        "event": "task_updated",
        "task_id": task.id,
        "status": task.status,
    })
    return task


def assign_task(org_id: int, task_id: int, task_assign: TaskAssign, db: Session):
    "Assign a task to an org member. Raises 404 if assignee not in org or task not found."
    assignee = db.query(OrganizationMember).filter(OrganizationMember.org_id == org_id,
                                                   OrganizationMember.user_id == task_assign.assigned_to).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found in organization")
    task = db.query(Task).filter(Task.id == task_id, Task.org_id == org_id, Task.is_deleted.is_(False)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assigned_to = task_assign.assigned_to
    db.commit()
    db.refresh(task)
    cache_delete_pattern(f"tasks:org:{org_id}:*")
    return task


def delete_task(org_id: int, task_id: int, db: Session):
    "Soft delete a task by setting is_deleted=True. Raises 404 if task not found or already deleted."
    task = db.query(Task).filter(Task.id == task_id, Task.org_id == org_id, Task.is_deleted.is_(False)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_deleted = True
    task.deleted_at = datetime.now(timezone.utc)
    db.commit()
    cache_delete_pattern(f"tasks:org:{org_id}:*")
    return {"message": "Task deleted!"}
