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
    return db.query(Place).all()

@router.post(
    "/",
    summary="Create a new place",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    new_place = Place(**place.dict())
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

@router.get(
    "/{place_id}",
    summary="Get a place by ID",
    response_model=PlaceResponse
)
async def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place

@router.patch(
    "/{place_id}",
    summary="Update a place",
    response_model=PlaceResponse
)
async def update_place(place_id: int, place: PlaceUpdate, db: Session = Depends(get_db)):
    db_place = db.query(Place).filter(Place.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    update_data = place.dict(exclude_unset = True)

    for key, value in update_data.items():
        setattr(db_place, key, value)

    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@router.delete(
    "/{place_id}",
    summary="Delete a place",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place.id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    db.delete(place)
    db.commit()
    return
