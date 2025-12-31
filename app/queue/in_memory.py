from queue import Queue
from uuid import UUID
from .base import JobQueue

# local testing only
class InMemoryJobQueue(JobQueue):
    def __init__(self):
        self._queue: Queue[UUID] = Queue()

    def enqueue(self, job_id: UUID) -> None:
        self._queue.put(job_id)

    def dequeue(self) -> UUID | None:
        if self._queue.empty():
            return None
        return self._queue.get()
