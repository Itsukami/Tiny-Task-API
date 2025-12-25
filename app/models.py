from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class TaskBase(BaseModel):
    """Base schema for shared data."""
    title: str = Field(..., min_length=1, max_length=120, description="Task title (1-120 chars)")

class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating a task. Fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    done: Optional[bool] = None

class TaskResponse(TaskBase):
    """Schema for reading a task (output)."""
    id: int
    done: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)