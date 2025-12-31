from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.schemas.job import Job, JobCreate
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Job as JobModel, JobStatus
import time
from uuid import UUID
from app.queue import job_queue

MAX_RETRIES = 3
RETRY_DELAY = 5 # seconds

# Create router
router = APIRouter(prefix="/jobs", tags=["jobs"])

# Post a new job
@router.post("/", response_model=Job)
def create_job(job: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_job = JobModel(
        task_name = job.task_name,
        payload = job.payload,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Run job in background
    # background_tasks.add_task(process_job, job_id = db_job.id)

    job_queue.enqueue(db_job.id)

    return db_job

# Fetch an existing job
@router.get("/{job_id}", response_model=Job)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail = "Job not found")
    return job

# Process background tasks
def process_job(job_id: UUID):
    # Create a fresh session for this thread
    db = next(get_db())
    try:
        # Updates status from pending -> running -> completed
        job = db.query(JobModel).filter(JobModel.id == job_id).first()
        if not job:
            return

        job.status = JobStatus.running
        db.commit()
        db.refresh(job)
        attempt = 0
        while attempt < MAX_RETRIES:
            try:
                # simulate doing work (replace this with real task)
                print(f"Running job {job.id}, attempt {attempt+1}")
                time.sleep(15)

                # Mark as completed
                job.status = JobStatus.completed
                db.commit()
                db.refresh(job)
                return
            except Exception as e:
                attempt += 1
                job.retry_count = attempt
                db.commit()
                db.refresh(job)
                time.sleep(RETRY_DELAY)

        job.status = JobStatus.failed
        db.commit()
        db.refresh(job)
    finally:
        db.close()
