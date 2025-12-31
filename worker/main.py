import time
from uuid import UUID

from app.queue import job_queue
from app.db.session import SessionLocal
from app.db.models import Job, JobStatus


def process_message(message):
    job_id = UUID(message["Body"])
    receipt_handle = message["ReceiptHandle"]

    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        job.status = JobStatus.running
        db.commit()

        time.sleep(5)  # simulate work

        job.status = JobStatus.completed
        db.commit()

        # ✅ ACK message
        job_queue.client.delete_message(
            QueueUrl=job_queue.client.meta.endpoint_url,
            ReceiptHandle=receipt_handle,
        )

        print(f"✅ Job {job_id} completed")

    except Exception as e:
        print(f"❌ Job {job_id} failed: {e}")
        # DO NOT delete message — visibility timeout handles retry

    finally:
        db.close()


def run_worker():
    print("👷 Worker listening to SQS...")
    while True:
        message = job_queue.dequeue()
        if message:
            process_message(message)


if __name__ == "__main__":
    run_worker()
