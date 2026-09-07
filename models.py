from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Name of the task"
    )
    description: str | None = Field(
        default=None,
        max_length=300,
        description="Task description"
    )

class TaskCreate(TaskBase):
    completed: bool = False
              
class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at : datetime

class TaskUpdate(TaskBase):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Name of the task"
    )
    description: str | None = Field(
        default=None,
        max_length=300,
        description="Task description"
    )
    completed: bool | None = None

