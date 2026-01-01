# Async Job Processor (FastAPI + AWS SQS + ECS)

An asynchronous job processing system built with FastAPI, PostgreSQL, AWS SQS, and ECS Fargate.
Designed to demonstrate distributed systems fundamentals, fault tolerance, and cloud-native architecture.

## Features

- FastAPI-based job submission API
- Persistent job state stored in PostgreSQL
- Distributed workers powered by AWS SQS
- Retry logic with configurable max retries
- Dead Letter Queue for failed jobs
- Horizontally scalable ECS Fargate workers
- Clean separation between API and worker services

## Architecture Overview
```mermaid
graph TD;
Client-->API;
API-->Database;
API-->Queue;
Queue-->Worker;
Worker-->Database;
```
### Key Design Decisions

- SQS ensures reliable message delivery and backpressure handling
- ECS Fargate enables stateless, auto-scalable workers
- Database-backed job state allows observability and recovery
- Retries handled explicitly instead of hidden magic
- DLQ preserves failed jobs for inspection

## Configuration
Environment variables are used for configration

### Required Variables
```
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/jobs
AWS_REGION=us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<account-id>/jobs
```
## Local Development

### Start services

```
docker-compose up --build
```

### Run migrations
```
alembic upgrade head
```

### Start API
```
uvicorn app.main:app --reload
```

### Start worker
Open separate terminal
```
python -m worker.main
```

## API Endpoints
### Create Job
```
Post /jobs
```
```
{
  "task_name": "send_email",
  "payload": { "user_id": 123 }
}
```
### Get Job Status
```
GET /jobs/{job_id}
```

### Retry & Failure Handling
- Jobs retry automatically on failure
- Retry count stored in DB
- Messages exceeding `MAX_JOB_RETRIES` marked as failed, removed from main queue, and sent to Dead Letter Queue

## AWS Deployment

### Services Used:
- Amazon SQS - job queue + DLQ
- Amazon ECS (Fargate) - worker service
- Amazon ECR - container registry

### Worker Deployment Flow
1. Build Docker image
2. Push to ECR
3. Register ECS Task definition
4. Run ECS service
5. Workers poll SQS continuously

## Scaling
Workers can be horizontally scaled by:
- Increasing ECS service desired count

## Possible Extensions
- Auto-scale workers based on queue depth
- Job prioritization
- Job cancellation
- Metrics endpoint
