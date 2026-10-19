

from uuid import uuid4

from fastapi import FastAPI, HTTPException

from app.schemas import EmailRequest, EmailDraftResponse
from app.database import (
    init_db,
    save_email,
    get_email,
    update_draft,
    approve_email,
)

app = FastAPI(
    title="Inbox Agent",
    description="Customer email intake and draft review API",
    version="0.2.0",
)

init_db()


@app.get("/")
async def home():
    return {
        "message": "Inbox Agent API is running!",
        "task": "Task 2",
        "status": "success",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/emails", response_model=EmailDraftResponse)
async def create_email(email: EmailRequest):
    email_id = str(uuid4())

    save_email(
        email_id=email_id,
        customer_name=email.customer_name,
        subject=email.subject,
        body=email.body,
    )

    return EmailDraftResponse(
        email_id=email_id,
        customer_name=email.customer_name,
        subject=email.subject,
        draft_reply="Email received. AI draft is not generated yet.",
        status="pending_review",
        approved=False,
    )


@app.get("/emails/{email_id}")
async def read_email(email_id: str):
    email = get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    return email


@app.put("/emails/{email_id}/draft")
async def save_email_draft(email_id: str, draft_reply: str):
    if not draft_reply.strip():
        raise HTTPException(
            status_code=400,
            detail="Draft cannot be empty",
        )

    if get_email(email_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    update_draft(email_id, draft_reply)

    return {
        "email_id": email_id,
        "status": "pending_review",
        "message": "Draft saved for human review.",
    }


@app.post("/emails/{email_id}/approve")
async def approve_email_draft(email_id: str):
    if not approve_email(email_id):
        raise HTTPException(
            status_code=400,
            detail="Email not found or draft is missing",
        )

    return {
        "email_id": email_id,
        "status": "approved",
        "message": "Draft approved by human reviewer.",
    }
