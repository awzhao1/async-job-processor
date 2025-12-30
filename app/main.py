from fastapi import FastAPI
from app.api.jobs import router as jobs_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async Job Processor")

app.include_router(jobs_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
