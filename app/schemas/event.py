from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    place_id: int
    title: str
    start_time: datetime
    remaining_seats: int

class EventUpdate(BaseModel):
    title: str | None = None
    start_time: datetime | None = None
    remaining_seats: int | None = None

class EventResponse(BaseModel):
    id: int
    place_id: int
    title: str
    start_time: datetime
    remaining_seats: int
    created_at: datetime

    class Config:
        from_attributes = True
