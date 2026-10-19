
from datetime import datetime
from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    """Incoming customer email."""

    customer_name: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    body: str = Field(min_length=5)
    received_at: datetime | None = None


class EmailDraftResponse(BaseModel):
    """Draft reply for human review."""

    email_id: str
    customer_name: str
    subject: str
    draft_reply: str
    status: str = "pending_review"
    approved: bool = False
