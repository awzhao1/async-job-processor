from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import datetime


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class JobCreate(BaseModel):
    task_name: str = Field(..., example="send_email")
    payload: dict = Field(..., example={"user_id": 123})


class Job(JobCreate):
    id: UUID = Field(default_factory=uuid4)
    status: JobStatus = JobStatus.pending
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
