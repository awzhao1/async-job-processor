from fastapi import FastAPI
from app.api.jobs import router as jobs_router

app = FastAPI(title="Async Job Processor")

app.include_router(jobs_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
