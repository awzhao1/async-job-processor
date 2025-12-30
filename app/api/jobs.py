from fastapi import APIRouter, Depends, HTTPException
from app.schemas.job import Job, JobCreate
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Job as JobModel


# Create router
router = APIRouter(prefix="/jobs", tags=["jobs"])

# TEMP in-memory store (will be replaced later)
JOBS: dict = {}

# Post a new job
@router.post("/", response_model=Job)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobModel(
        task_name = job.task_name,
        payload = job.payload,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# Fetch an existing job
@router.get("/{job_id}", response_model=Job)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail = "Job not found")
    return job
