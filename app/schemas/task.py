from pydantic import BaseModel
from datetime import date
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    project_id: int
    assigned_to: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = "in_progress"
    due_date: Optional[date] = None