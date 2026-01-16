from datetime import datetime, timedelta
from fastapi import status

def test_create_event(client):
    # Need a place first
    client.post(
        "/places/",
        json={
            "name": "Event Venue",
            "category": "Hall",
            "latitude": 37.0,
            "longitude": 127.0,
        },
    )
    
    response = client.post(
        "/events/",
        json={
            "place_id": 1,
            "title": "Concert",
            "start_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "remaining_seats": 100,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Concert"
    assert "id" in data

def test_list_events(client):
    response = client.get("/events/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_event(client):
    # Create
    create_res = client.post(
        "/events/",
        json={
            "place_id": 1,
            "title": "Get Event",
            "start_time": datetime.utcnow().isoformat(),
            "remaining_seats": 50,
        },
    )
    event_id = create_res.json()["id"]

    # Get
    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Get Event"
    assert data["id"] == event_id

def test_update_event(client):
    # Create
    create_res = client.post(
        "/events/",
        json={
            "place_id": 1,
            "title": "Old Title",
            "start_time": datetime.utcnow().isoformat(),
            "remaining_seats": 10,
        },
    )
    event_id = create_res.json()["id"]

    # Update
    response = client.patch(
        f"/events/{event_id}",
        json={"title": "New Title"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "New Title"
    assert data["remaining_seats"] == 10

def test_delete_event(client):
    # Create
    create_res = client.post(
        "/events/",
        json={
            "place_id": 1,
            "title": "Delete Event",
            "start_time": datetime.utcnow().isoformat(),
            "remaining_seats": 0,
        },
    )
    event_id = create_res.json()["id"]

    # Delete
    response = client.delete(f"/events/{event_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify
    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_events_by_place(client):
    # NOTE: The implementation in events.py has a route prefix issue:
    # router prefix is "/events", so the path becomes "/events/places/{place_id}/events"
    # unless handled otherwise. Let's test based on the current implementation.
    # The code has `@router.get("/places/{place_id}/events")` inside `events.py`.
    # So the URL is likely `/events/places/{place_id}/events`.
    
    response = client.get("/events/places/1/events")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
