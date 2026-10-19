
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "inbox.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS emails (
                email_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                draft_reply TEXT,
                status TEXT NOT NULL DEFAULT 'received',
                approved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_email(email_id, customer_name, subject, body):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO emails
            (email_id, customer_name, subject, body)
            VALUES (?, ?, ?, ?)
            """,
            (email_id, customer_name, subject, body),
        )


def get_email(email_id):
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM emails WHERE email_id = ?",
            (email_id,),
        ).fetchone()

    return dict(row) if row else None

def update_draft(email_id, draft_reply):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            UPDATE emails
            SET draft_reply = ?, status = 'pending_review',
                approved = 0
            WHERE email_id = ?
            """,
            (draft_reply, email_id),
        )
        return cursor.rowcount > 0


def approve_email(email_id):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            UPDATE emails
            SET approved = 1, status = 'approved'
            WHERE email_id = ? AND draft_reply IS NOT NULL
            """,
            (email_id,),
        )
        return cursor.rowcount > 0
