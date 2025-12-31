from abc import ABC, abstractmethod
from uuid import UUID

class JobQueue(ABC):
    @abstractmethod
    def enqueue(self, job_id: UUID) -> None:
        pass

    @abstractmethod
    def dequeue(self) -> UUID | None:
        pass
