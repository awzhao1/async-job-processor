import boto3
from uuid import UUID
from .base import JobQueue

class SQSJobQueue(JobQueue):
    def __init__(self, queue_url: str, region: str = "us-east-1"):
        self.client = boto3.client("sqs", region_name=region)
        self.queue_url = queue_url

    def enqueue(self, job_id: UUID) -> None:
        self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=str(job_id)
        )

    def dequeue(self) -> tuple[UUID, str] | None:
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        messages = response.get("Messages", [])
        if not messages:
            return None

        msg = messages[0]
        return UUID(msg["Body"]), msg["ReceiptHandle"]

    def delete(self, receipt_handle: str) -> None:
        self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
