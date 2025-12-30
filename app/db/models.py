import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from enum import Enum as PyEnum

# Enumeration of job status again
class JobStatus(str, PyEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

# Job Table
class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_name = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(
        Enum(JobStatus, name="job_status"),
        default=JobStatus.pending,
        nullable=False,
    )
    created_at = Column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
