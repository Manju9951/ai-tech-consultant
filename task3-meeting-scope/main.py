@'
from fastapi import FastAPI

app = FastAPI(
    title="Meeting to Scope of Work",
    description="AI-powered consultant for client meetings and project scope",
    version="0.1.0",
)


@app.get("/")
async def home():
    return {
        "message": "Meeting to Scope of Work API is running!",
        "project": "Task 3",
        "status": "success",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "meeting-scope-api",
    }
'@ | Set-Content -Encoding utf8 app\main.py