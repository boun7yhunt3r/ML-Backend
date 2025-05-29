from pydantic import BaseModel, Field
from enum import Enum

class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class EventCreate(BaseModel):
    event_id: str = Field(..., min_length=1, max_length=50)
    timestamp: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    severity: Severity
    description: str = Field(..., min_length=1)