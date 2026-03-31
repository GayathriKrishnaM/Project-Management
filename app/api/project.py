from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.user import User
from app.db.dependencies import get_db
from app.api.auth import get_current_user
from app.core.roles import ADMIN

router = APIRouter()

@router.post("/")
def create_project(
    name: str = Body(..., min_length=3),
    description: str = Body(..., min_length=3),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = Project(
        name=name,
        description=description,
        created_by=current_user.id
    )
    try:
        db.add(project)
        db.commit()
        db.refresh(project)
    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to create project")
    return project

@router.get("/")
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Project).all()
    
    
@router.put("/{project_id}")
def update_project(project_id: int, name: str = Body(..., min_length=3), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    if current_user.role != ADMIN and project.created_by != current_user.id:
        raise HTTPException(403, "Not allowed")

    project.name = name
    try:
        db.commit()
        db.refresh(project)
    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to update project")

    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    if current_user.role != ADMIN and project.created_by != current_user.id:
        raise HTTPException(403, "Not allowed")

    
    try:
        db.delete(project)
        db.commit()
        return {"message": "Project deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to delete project")
