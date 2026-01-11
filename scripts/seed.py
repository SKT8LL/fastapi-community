from app.db import SessionLocal, engine, Base
from app.models.place import Place
from app.models.event import Event
from app.models.deal import Deal
from app.models.docent import Docent
from datetime import datetime, timedelta
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def seed_data():
    db = SessionLocal()
    
    # Create tables if not exist (mostly for local testing)
    Base.metadata.create_all(bind=engine)

    # Check if data exists
    if db.query(Place).count() > 0:
        print("Data already exists. Skipping seed.")
        return

    # Places
    place1 = Place(
        name="Club Evans", 
        category="band_club", 
        tags="jazz,indie,live",
        latitude=37.555, 
        longitude=126.920
    )
    place2 = Place(
        name="Cinema 404", 
        category="cinema", 
        tags="indie,art,classic",
        latitude=37.560, 
        longitude=126.925
    )
    db.add_all([place1, place2])
    db.commit()
    db.refresh(place1)
    db.refresh(place2)

    # Events
    event1 = Event(
        place_id=place1.id, 
        title="Jazz Night", 
        start_time=datetime.utcnow() + timedelta(days=1),
        remaining_seats=20
    )
    event2 = Event(
        place_id=place2.id, 
        title="Midnight Movie", 
        start_time=datetime.utcnow() + timedelta(hours=5),
        remaining_seats=50
    )
    db.add_all([event1, event2])
    db.commit()
    db.refresh(event1)
    db.refresh(event2)

    # Deals
    deal1 = Deal(
        event_id=event1.id,
        discount_rate=30,
        starts_at=datetime.utcnow(),
        ends_at=event1.start_time
    )
    db.add(deal1)

    # Docents
    docent1 = Docent(
        place_id=place1.id,
        tone="energetic",
        content="This place is full of vibrant jazz energy! You'll love the saxophone solos."
    )
    db.add(docent1)

    db.commit()
    print("Seed data created successfully.")
    db.close()

if __name__ == "__main__":
    # 로컬 테스트용입니다. 배포 환경에서는 실행하지 마세요.
    seed_data()
