from fastapi import APIRouter
from app.schemas.job import Job, JobCreate

router = APIRouter(prefix="/jobs", tags=["jobs"])

# TEMP in-memory store (will be replaced later)
JOBS: dict = {}


@router.post("/", response_model=Job)
def create_job(job: JobCreate):
    new_job = Job(**job.model_dump())
    JOBS[str(new_job.id)] = new_job
    return new_job


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: str):
    return JOBS[job_id]
