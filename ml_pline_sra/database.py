import sqlite3
from typing import List, Tuple

def init_db():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            event_id TEXT PRIMARY KEY,
            request_size REAL NOT NULL,
            response_time REAL NOT NULL,
            is_risky INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_prediction(event_id: str, request_size: float, response_time: float, is_risky: int, timestamp: str):
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (event_id, request_size, response_time, is_risky, timestamp) VALUES (?, ?, ?, ?, ?)",
        (event_id, request_size, response_time, is_risky, timestamp)
    )
    conn.commit()
    conn.close()

def get_predictions() -> List[Tuple]:
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions")
    predictions = cursor.fetchall()
    conn.close()
    return predictions