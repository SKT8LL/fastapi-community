from pydantic import BaseModel
from datetime import datetime

class DocentCreate(BaseModel):
    place_id: int
    tone: str
    content: str

class DocentResponse(BaseModel):
    id: int
    place_id: int
    tone: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
