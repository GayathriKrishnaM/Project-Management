from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.dependencies import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.api.auth import get_current_user
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate  
from datetime import date
from app.core.roles import ADMIN

router = APIRouter(tags=["Tasks"])

VALID_STATUS = ["pending", "in_progress", "done", "completed", "cancelled"]

@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != ADMIN and project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    assigned_user_id = None

    if task.assigned_to:

        user = db.query(User).filter(
            User.id == task.assigned_to
        ).first()

        if not user:
            raise HTTPException(404, "Assigned user not found")

        if user.role == ADMIN:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign task to admin"
            )

        assigned_user_id = user.id
        
    if task.status and task.status not in VALID_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")

    if task.due_date and task.due_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Due date cannot be in the past"
        )

    new_task = Task(
        title=task.title,
        project_id=task.project_id,
        assigned_to=assigned_user_id,   
        description=task.description,
        status=task.status,
        due_date=task.due_date
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create task")

    return new_task

@router.patch("/{task_id}/assign")
def assign_task(
    task_id: int,
    user_id: int | None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(404, "Task not found")

    project = db.query(Project).filter(
        Project.id == task.project_id
    ).first()

    is_admin = current_user.role == ADMIN
    is_project_creator = project.created_by == current_user.id

    if not (is_admin or is_project_creator):
        raise HTTPException(
            status_code=403,
            detail="Not allowed to assign task"
        )

    if user_id is None:
        task.assigned_to = None

    else:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(404, "User not found")

        task.assigned_to = user.id

    try:
        db.commit()
        db.refresh(task)
    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to assign task")

    return task

@router.patch("/{task_id}/status")
def update_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(404, "Task not found")

    if status not in VALID_STATUS:
        raise HTTPException(400, "Invalid status")

    if current_user.role != ADMIN and task.assigned_to != current_user.id:
        raise HTTPException(403, "Not allowed")

    task.status = status
    try:
        db.commit()
        db.refresh(task)
    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to update status")

    return task

@router.get("/")
def list_tasks(
    project_id: int = None,
    status: str = None,
    assigned_to: int = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)

    if status:
        query = query.filter(Task.status == status)

    if assigned_to and current_user.role == ADMIN:
        query = query.filter(Task.assigned_to == assigned_to)

    total = query.count()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "tasks": query.offset(offset).limit(limit).all()
    }