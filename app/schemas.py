# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    completed: bool
    # created_at/updated_at may be None immediately after creation (DB may not set updated_at on insert)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Enables ORM mode / attribute access. Keep both keys for compatibility across Pydantic versions.
        from_attributes = True
        orm_mode = True
