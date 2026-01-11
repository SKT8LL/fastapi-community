from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Docent(Base):
    __tablename__ = "docents"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"))
    tone = Column(String(50))  # energetic, serene, cultural
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    place = relationship("Place", back_populates="docents")
