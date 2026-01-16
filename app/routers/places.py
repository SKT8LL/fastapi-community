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
    """Get all places.
    
    데이터베이스에 저장된 모든 장소(Places) 목록을 조회합니다.
    """
    # DB의 'places' 테이블에서 모든 데이터(all)를 조회(select)해서 반환합니다.
    # SELECT * FROM places; 쿼리와 동일합니다.
    return db.query(Place).all()

@router.post(
    "/",
    summary="Create a new place",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    """Create a new place.
    
    새로운 장소를 생성하고 DB에 저장합니다.
    """
    # 1. 입력받은 Pydantic 모델(place)을 DB 모델(Place)로 변환합니다.
    # **place.dict()는 딕셔너리 언패킹을 통해 필드 값을 자동으로 매핑해줍니다.
    new_place = Place(**place.dict())
    
    # 2. 세션(임시 저장소)에 추가합니다.
    db.add(new_place)
    
    # 3. 실제 DB에 변경 사항을 영구 저장(Commit)합니다.
    db.commit()
    
    # 4. DB에 저장된 최신 정보(ID, 생성시간 등)를 받아와서 객체를 업데이트합니다.
    db.refresh(new_place)
    
    return new_place

@router.get(
    "/{place_id}",
    summary="Get a place by ID",
    response_model=PlaceResponse
)
async def get_place(place_id: int, db: Session = Depends(get_db)):
    """Get a place by ID.
    
    특정 ID를 가진 장소 하나를 상세 조회합니다.
    """
    # DB에서 ID가 일치하는 첫 번째(first) 데이터를 찾습니다.
    place = db.query(Place).filter(Place.id == place_id).first()
    
    # 만약 데이터가 없으면(None), 404 에러를 발생시킵니다.
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
        
    return place

@router.patch(
    "/{place_id}",
    summary="Update a place",
    response_model=PlaceResponse
)
async def update_place(place_id: int, place: PlaceUpdate, db: Session = Depends(get_db)):
    """Update a place.
    
    기존 장소 정보를 수정합니다. 입력된 필드만 부분적으로 업데이트합니다.
    """
    # 1. 수정할 대상을 먼저 찾습니다.
    db_place = db.query(Place).filter(Place.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    
    # 2. 사용자가 보낸 데이터 중, 실제로 값이 있는 것만 골라냅니다 (exclude_unset=True).
    # None으로 덮어써지는 것을 방지합니다.
    update_data = place.dict(exclude_unset = True)

    # 3. 반복문으로 바꿀 필드만 쏙쏙 값을 변경합니다.
    # setattr(객체, '필드명', 값) -> db_place.필드명 = 값
    for key, value in update_data.items():
        setattr(db_place, key, value)

    # 4. 변경된 내용을 저장합니다.
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
    """Delete a place.
    
    장소를 삭제합니다.
    """
    # 1. 삭제할 대상을 찾습니다. (주의: filter 안에 복사-붙여넣기 실수로 Place.id == place.id 같은 코드가 없는지 확인!)
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    
    # 2. 대상을 삭제 목록에 추가합니다.
    db.delete(place)
    
    # 3. 실제 DB에 반영합니다.
    db.commit()
    
    return
