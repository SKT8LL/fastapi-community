from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.deal import Deal
from app.schemas.deal import DealCreate, DealResponse
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get(
    "/",
    summary="List all deals",
    response_model=list[DealResponse]
)
async def list_deals(db: Session = Depends(get_db)):
    # TODO
    return db.query(Deal).all() # db.query()를 통해 Deal에 있는 모든 데이터들을 가져온다.

@router.post(
    "/",
    summary="Create a new deal",
    response_model=DealResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_deal(deal: DealCreate, db: Session = Depends(get_db)):
    # TODO
    new_deal = Deal(**deal.dict()) # deal를 처리할 수 있는 형태로.
    db.add(new_deal) # DB 세션에 추가.
    db.commit() # 변경사항 저장.
    db.refresh(new_deal) # 갱신

    return new_deal

@router.get(
    "/{deal_id}",
    summary="Get a deal",
    response_model=DealResponse
)
async def get_deal(deal_id: int, db: Session = Depends(get_db)):
    # TODO
    deal = db.query(Deal).filter(Deal.id == deal_id).first() # deal_id인 멤버를 DB에서 찾기.

    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")

    return deal    
   

@router.delete(
    "/{deal_id}",
    summary="Delete a deal",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    # TODO

    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")

    db.delete(deal)
    db.commit()

# Special endpoint: Recommend Deal
class DealRecommendInput(BaseModel):
    event_id: int
    remaining_seats: int
    minutes_to_start: int
    total_capacity: int

class DealRecommendOutput(BaseModel):
    discount_rate: int
    discounted_price: int
    expires_at: datetime

@router.post(
    "/recommend",
    summary="Recommend dynamic discount",
    response_model=DealRecommendOutput
)
async def recommend_deal(input: DealRecommendInput):
    """
    Calculate dynamic discount rate based on occupancy and time left.
    Stub logic: discount_rate = (occupancy_rate * 20) + (minutes_to_start * 2)
    """
    if input.total_capacity == 0:
        occupancy_rate = 1
    else:
        occupancy_rate = (input.total_capacity - input.remaining_seats) / input.total_capacity
    
    # Simple stub calculation
    # minutes_to_start * 2 logic seems weird if it increases discount as time remains more?
    # Usually less time = more discount. But prompt says "minutes_to_start * 2".
    # I will follow prompt example exactly.
    # Prompt: discount_rate = (occupancy_rate * 20) + (minutes_to_start * 2)
    
    raw_discount = (occupancy_rate * 20) + (input.minutes_to_start * 2)
    discount_rate = min(int(raw_discount), 100)
    
    # Stub price (e.g. base 10000)
    base_price = 10000
    discounted_price = int(base_price * (100 - discount_rate) / 100)
    
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    return {
        "discount_rate": discount_rate,
        "discounted_price": discounted_price,
        "expires_at": expires_at
    }
