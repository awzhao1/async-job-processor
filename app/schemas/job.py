# app/schemas/job.py
from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
import datetime

class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class JobCreate(BaseModel):
    task_name: str
    payload: dict

class Job(JobCreate):
    id: UUID
    status: JobStatus
    created_at: datetime.datetime
