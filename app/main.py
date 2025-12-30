from fastapi import FastAPI

app = FastAPI(title="Async Job Processor")

@app.get("/health")
def health_check():
    return {"status": "ok"}
