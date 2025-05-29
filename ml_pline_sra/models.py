from pydantic import BaseModel

class EventInput(BaseModel):
    request_size: float
    response_time: float