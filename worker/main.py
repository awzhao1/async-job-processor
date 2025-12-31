from time import sleep
from app.queue import job_queue
from app.db.session import SessionLocal
from app.db.models import Job, JobStatus
from uuid import UUID
from app.core.config import settings

def process_message(job_id: UUID, receipt_handle: str):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        job.status = JobStatus.running
        db.commit()

        # Simulated work
        sleep(10)

        # raise RuntimeError("Simulated failure")  # Uncomment to test retries

        job.status = JobStatus.completed
        db.commit()

        # ACK success
        job_queue.delete(receipt_handle)

    except Exception as e:
        job.retry_count += 1
        if job.retry_count >= settings.max_job_retries:
            job.status = JobStatus.failed
            db.commit()
            job_queue.delete(receipt_handle)
            print(f"☠️ Job {job_id} permanently failed")
        else:
            job.status = JobStatus.pending
            db.commit()
            print(f"🔁 Job {job_id} failed — retry {job.retry_count}/{settings.max_job_retries}")

    finally:
        db.close()


def worker_loop():
    print("Worker started, polling SQS...")
    while True:
        item = job_queue.dequeue()  # <-- use dequeue(), not receive_messages()
        if item is None:
            sleep(2)
            continue

        job_id, receipt_handle = item
        process_message(job_id, receipt_handle)


if __name__ == "__main__":
    worker_loop()
