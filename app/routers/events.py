from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix="/events", tags=["events"])

@router.get(
    "/",
    summary="List all events",
    response_model=list[EventResponse]
)
async def list_events(db: Session = Depends(get_db)):
    """List all events.
    
    모든 이벤트 목록을 조회합니다.
    """
    # DB의 'events' 테이블에서 모든 데이터(all)를 조회(select)해서 반환합니다.
    # SELECT * FROM events;
    return db.query(Event).all()

@router.post(
    "/",
    summary="Create a new event",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Create a new event.
    
    새로운 이벤트를 생성합니다.
    """
    # 1. Pydantic 모델(event)을 DB 모델(Event)로 변환합니다.
    new_event = Event(**event.dict())
    
    # 2. 세션에 추가하고 저장(Commit)합니다.
    db.add(new_event)
    db.commit()
    
    # 3. 생성된 데이터(ID 등)를 최신화합니다.
    db.refresh(new_event)
    
    return new_event

@router.get(
    "/{event_id}",
    summary="Get an event",
    response_model=EventResponse
)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get an event.
    
    특정 ID의 이벤트를 상세 조회합니다.
    """
    # ID가 일치하는 이벤트를 찾습니다.
    event = db.query(Event).filter(Event.id == event_id).first()
    
    # 없으면 404 에러를 반환합니다.
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        
    return event

@router.patch(
    "/{event_id}",
    summary="Update an event",
    response_model=EventResponse
)
async def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    """Update an event.
    
    이벤트 정보를 수정합니다.
    """
    # 1. 수정할 이벤트를 찾습니다.
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    # 2. 업데이트할 데이터만 추출합니다 (exclude_unset=True).
    update_data = event.dict(exclude_unset=True)
    
    # 3. 값을 변경합니다.
    for key, value in update_data.items():
        setattr(db_event, key, value)
        
    # 4. 저장합니다.
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.delete(
    "/{event_id}",
    summary="Delete an event",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event.
    
    이벤트를 삭제합니다.
    """
    # 1. 삭제할 이벤트를 찾습니다.
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    # 2. 삭제하고 커밋합니다.
    db.delete(event)
    db.commit()
    
    return

# Special endpoint: Get events by place
@router.get(
    "/places/{place_id}/events",
    summary="List events for a place",

                     
    response_model=list[EventResponse]
)
async def list_events_by_place(place_id: int, db: Session = Depends(get_db)):
    """List events for a place.

    특정 장소(Place)에 속한 이벤트 목록을 조회합니다.
    """
    # 'place_id'가 일치하는 이벤트들만 필터링해서 가져옵니다.
    # SELECT * FROM events WHERE place_id = {place_id};
    return db.query(Event).filter(Event.place_id == place_id).all()
# Wait, if I want it to be /places/{place_id}/events, and keeping it in events.py:
# I can instantiate another router or just add it to the main `app` in `main.py` directly from events.py? No.
# Best practice: `events.router` handles `/events`.
# `places.router` handles `/places`.
# So update `places.py` to include this endpoint? But that edits `places.py`. A does both.
# Okay, I will add it to `app/routers/places.py` instead, as it technically falls under `/places` prefix.
# "A 담당자" does both files anyway.
# I will edit `app/routers/places.py` to add `GET /{place_id}/events`.
# But wait, I just wrote `app/routers/places.py` in this turn.
# I can't edit it in the same turn easily if I didn't verify it.
# Actually I can use `write_to_file` again to overwrite `app/routers/places.py` with the additional endpoint, 
# OR I can just stick to `events.py` and define a router that handles it.
# Check `main.py`: `app.include_router(events.router)`.
# If `events.router` has prefix `/events`, then I can't do `/places/...`.
# I will make `events.py` export TWO routers? Or just one router with NO prefix, and I specify path manually?
# In `main.py`: `app.include_router(events.router)`.
# Let's check `antigravity_prompt.md` line 239 `router = APIRouter(prefix="/places", tags=["places"])`.
# So `places.py` has prefix.
# `events.py` likely has `prefix="/events"`.
# So `/places/{place_id}/events` naturally belongs in `places.py`.
# I will overwrite `app/routers/places.py` to include it.
# AND I should define `app/routers/events.py` as well.
# I will write `events.py` first, then overwrite `places.py` including the relationship logic.
