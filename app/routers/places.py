from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.place import Place
from app.schemas.place import PlaceCreate, PlaceUpdate, PlaceResponse

router = APIRouter(prefix="/places", tags=["places"])

@router.get(
    "/",
    summary="List all places",
    description="Retrieve all culture spaces",
    response_model=list[PlaceResponse],
    status_code=status.HTTP_200_OK
)
async def list_places(db: Session = Depends(get_db)):
    """Get all places."""
    # TODO: Query DB and return list
    return []

@router.post(
    "/",
    summary="Create a new place",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    """Create a new place."""
    # TODO: Create and save to DB
    raise NotImplementedError("TODO: Implement place creation")

@router.get(
    "/{place_id}",
    summary="Get a place by ID",
    response_model=PlaceResponse
)
async def get_place(place_id: int, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO: Implement get place")

@router.patch(
    "/{place_id}",
    summary="Update a place",
    response_model=PlaceResponse
)
async def update_place(place_id: int, place: PlaceUpdate, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO: Implement update place")

@router.delete(
    "/{place_id}",
    summary="Delete a place",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_place(place_id: int, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO: Implement delete place")
