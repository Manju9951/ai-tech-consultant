
from datetime import datetime
from pydantic import BaseModel, Field


class MeetingRequest(BaseModel):
    """Input details for a client meeting transcript."""

    client_name: str = Field(
        min_length=1,
        description="Name of the client or company",
    )
    meeting_title: str = Field(
        min_length=1,
        description="Title or purpose of the meeting",
    )
    transcript: str = Field(
        min_length=20,
        description="Raw client meeting transcript",
    )
    meeting_date: datetime | None = None


class MeetingResponse(BaseModel):
    """Response after accepting a meeting transcript."""

    meeting_id: str
    client_name: str
    meeting_title: str
    status: str
    message: str
