from pydantic import BaseModel
from datetime import datetime

class DealCreate(BaseModel):
    event_id: int
    discount_rate: int
    starts_at: datetime
    ends_at: datetime

class DealResponse(BaseModel):
    id: int
    event_id: int
    discount_rate: int
    starts_at: datetime
    ends_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
