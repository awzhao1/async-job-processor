# worker/main.py
import time
from uuid import UUID

from app.db.session import SessionLocal
from app.db.models import Job, JobStatus
from app.queue import job_queue

POLL_INTERVAL = 2


def process_job(job_id: UUID):
    db = SessionLocal()

    try:
        job = db.get(Job, job_id)
        if not job:
            return

        job.status = JobStatus.running
        db.commit()

        # Simulate work
        time.sleep(10)

        job.status = JobStatus.completed
        db.commit()

    except Exception:
        job.status = JobStatus.failed
        db.commit()
    finally:
        db.close()


def run():
    while True:
        job_id = job_queue.dequeue()

        if job_id is None:
            time.sleep(POLL_INTERVAL)
            continue

        process_job(job_id)


if __name__ == "__main__":
    run()
