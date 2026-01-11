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
    # TODO
    return []

@router.post(
    "/",
    summary="Create a new event",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO")

@router.get(
    "/{event_id}",
    summary="Get an event",
    response_model=EventResponse
)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO")

@router.patch(
    "/{event_id}",
    summary="Update an event",
    response_model=EventResponse
)
async def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO")

@router.delete(
    "/{event_id}",
    summary="Delete an event",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO")

# Special endpoint: Get events by place
@router.get(
    "/places/{place_id}/events",
    summary="List events for a place",
    tags=["places"], # Or events, logic says it's about events in a place. But prompt says 'GET /places/{place_id}/events'. 
                     # However, to avoid circular import or router confusion, usually implemented in events router or places router.
                     # Prompt lists it under 'Events (A 담당자)'. So I implement it here.
                     # But path is /places/... so it might conflict if places router captures /places/{id} first.
                     # Places router prefix is /places. 
                     # If I put this in events router, I must use absolute path or include this router with different prefix?
                     # No, FastAPI allows multiple routers.
                     # But prefix '/events' makes it /events/places/{place_id}/events if I'm not careful.
                     # I should use `@router.get("/places/{place_id}/events", ...)` but wait, router prefix is `/events`.
                     # So it becomes `/events/places/{place_id}/events` which is wrong.
                     # It should be `/places/{place_id}/events`.
                     # So I should probably add another router for this specific path OR put it in places router.
                     # Guide says "Events (A 담당자)" implements it.
                     # I will put it in `app/routers/events.py` but use a separate router or modify prefix usage.
                     # Or just define it with absolute path? verify if APIRouter supports overriding prefix.
                     # Actually, usually such nested resources are better in the parent resource router (places).
                     # But the assignment says A does Events.
                     # Let's check `app/routers/places.py`... I already wrote it.
                     # I will add it to `app/routers/events.py` but bind it to a new router without prefix or just handle it.
                     # Simpler: Just put it in `places.py`? 
                     # No, A works on events.py too.
                     # Let's create a separate router in events.py that has no prefix, or handles /places/{place_id}/events.
                     
    response_model=list[EventResponse]
)
async def list_events_by_place(place_id: int, db: Session = Depends(get_db)):
    # TODO
    return []
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
