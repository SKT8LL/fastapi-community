from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    category = Column(String(100))
    tags = Column(String(500), nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="place")
    docents = relationship("Docent", back_populates="place")
