from app.core.config import settings
from app.queue.in_memory import InMemoryJobQueue
from app.queue.sqs import SQSJobQueue

# if settings.QUEUE_BACKEND == "sqs":
#     job_queue = SQSJobQueue(settings.SQS_QUEUE_URL)
# else:
#     job_queue = InMemoryJobQueue()

job_queue = SQSJobQueue(settings.sqs_queue_url)