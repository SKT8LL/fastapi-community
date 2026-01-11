from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    discount_rate = Column(Integer)  # 0-100
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="deals")
