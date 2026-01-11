from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"))
    title = Column(String(200), index=True)
    start_time = Column(DateTime)
    remaining_seats = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    place = relationship("Place", back_populates="events")
    # Deal relationship (optional, per Event, 1:1 or 1:N but logic says 'Last-minute 할인(특정 Event에 적용)')
    # Assuming 1:N or 1:1, let's say 1:1 for simplicity or 1:N.
    # Deal model has event_id.
    deals = relationship("Deal", back_populates="event")
