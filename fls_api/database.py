import sqlite3
from typing import Optional, List, Tuple

def init_db():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_event(event_id: str, timestamp: str, severity: str, description: str):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (event_id, timestamp, severity, description) VALUES (?, ?, ?, ?)",
        (event_id, timestamp, severity, description)
    )
    conn.commit()
    conn.close()

def get_events(severity: Optional[str] = None) -> List[Tuple]:
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    if severity:
        cursor.execute("SELECT * FROM events WHERE severity = ?", (severity,))
    else:
        cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return events