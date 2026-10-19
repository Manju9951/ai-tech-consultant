
from fastapi import FastAPI

app = FastAPI(
    title="AI Tech Consultant - Knowledge Brain",
    description="Knowledge Brain API",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Knowledge Brain API is running",
        "status": "starting",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
