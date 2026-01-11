from pydantic import BaseModel
from datetime import datetime

class PlaceCreate(BaseModel):
    name: str
    category: str
    tags: str | None = None
    latitude: float
    longitude: float

class PlaceUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    tags: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class PlaceResponse(BaseModel):
    id: int
    name: str
    category: str
    tags: str | None
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 호환성
