# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    # Added Field validation
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
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

# === Task Schemas (Enhanced) ===


class TaskBase(BaseModel):
    # Added Field validation
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    # Use Optional since it might be None initially
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# === User Schemas (New) ===


class UserBase(BaseModel):
    email: EmailStr  # Ensures the input is a valid email format


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Plain text password")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
