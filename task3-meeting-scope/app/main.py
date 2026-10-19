


from uuid import uuid4

from fastapi import FastAPI, HTTPException

from app.models.schemas import MeetingRequest, MeetingResponse
from app.services.database import init_db, save_meeting, get_meeting

app = FastAPI(
    title="Meeting to Scope of Work",
    description="AI-powered consultant for client meetings and project scope",
    version="0.1.0",
)

init_db()


@app.get("/")
async def home():
    return {
        "message": "Meeting to Scope of Work API is running!",
        "project": "Task 3",
        "status": "success",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/meetings", response_model=MeetingResponse)
async def create_meeting(meeting: MeetingRequest) -> MeetingResponse:
    meeting_id = str(uuid4())

    save_meeting(
        meeting_id=meeting_id,
        client_name=meeting.client_name,
        meeting_title=meeting.meeting_title,
        transcript=meeting.transcript,
        meeting_date=(
            meeting.meeting_date.isoformat()
            if meeting.meeting_date
            else None
        ),
    )

    return MeetingResponse(
        meeting_id=meeting_id,
        client_name=meeting.client_name,
        meeting_title=meeting.meeting_title,
        status="received",
        message="Meeting transcript saved successfully.",
    )


@app.get("/meetings/{meeting_id}")
async def read_meeting(meeting_id: str):
    meeting = get_meeting(meeting_id)

    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return meeting

    
