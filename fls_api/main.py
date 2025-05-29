from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import sqlite3
from typing import Optional
from database import init_db, insert_event, get_events

app = FastAPI(title="AI Firewall Logging System")

# API key for authentication
API_KEY = "secure-api-key-12345"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key

# Enum for severity levels
class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# Pydantic model for event input
class EventCreate(BaseModel):
    event_id: str = Field(..., min_length=1, max_length=50)
    timestamp: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    severity: Severity
    description: str = Field(..., min_length=1)

# Initialize database
init_db()

@app.post("/log-event")
async def log_event(event: EventCreate, api_key: str = Depends(verify_api_key)):
    try:
        # Validate ISO timestamp
        datetime.fromisoformat(event.timestamp.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    
    try:
        insert_event(event.event_id, event.timestamp, event.severity, event.description)
        return {"message": "Event logged successfully", "event_id": event.event_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Event ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/events")
async def list_events(severity: Optional[Severity] = None, api_key: str = Depends(verify_api_key)):
    events = get_events(severity)
    return {"events": [{"event_id": e[0], "timestamp": e[1], "severity": e[2], "description": e[3]} for e in events]}