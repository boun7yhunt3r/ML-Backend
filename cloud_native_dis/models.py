from pydantic import BaseModel, Field, validator
from datetime import datetime

class LogCreate(BaseModel):
    log_id: str = Field(..., min_length=1, max_length=50)
    source_ip: str = Field(..., min_length=7, max_length=15)
    event_type: str = Field(..., min_length=1, max_length=50)
    timestamp: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    @validator("source_ip")
    def validate_ip(cls, v):
        import ipaddress
        ipaddress.ip_address(v)
        return v

    @validator("timestamp")
    def validate_timestamp(cls, v):
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v