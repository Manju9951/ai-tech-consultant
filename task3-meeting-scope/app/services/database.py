
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "meetings.db"


def init_db() -> None:
    """Create the meetings table if it does not exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS meetings (
                meeting_id TEXT PRIMARY KEY,
                client_name TEXT NOT NULL,
                meeting_title TEXT NOT NULL,
                transcript TEXT NOT NULL,
                meeting_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_meeting(
    meeting_id: str,
    client_name: str,
    meeting_title: str,
    transcript: str,
    meeting_date: str | None = None,
) -> None:
    """Save a client meeting to SQLite."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO meetings (
                meeting_id, client_name, meeting_title,
                transcript, meeting_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                meeting_id,
                client_name,
                meeting_title,
                transcript,
                meeting_date,
            ),
        )


def get_meeting(meeting_id: str) -> dict | None:
    """Retrieve a saved meeting by its ID."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM meetings WHERE meeting_id = ?",
            (meeting_id,),
        ).fetchone()

    return dict(row) if row else None
