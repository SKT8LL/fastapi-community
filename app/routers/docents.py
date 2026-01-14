from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.docent import Docent
from app.schemas.docent import DocentCreate, DocentResponse
from pydantic import BaseModel

router = APIRouter(prefix="/docents", tags=["docents"])

@router.get(
    "/",
    summary="List all docents",
    response_model=list[DocentResponse]
)
async def list_docents(db: Session = Depends(get_db)):
    # TODO

    return db.query(Docent).all()

@router.post(
    "/",
    summary="Create a new docent",
    response_model=DocentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_docent(docent: DocentCreate, db: Session = Depends(get_db)):
    # TODO

    new_docent = Docent(**docent.dict())
    db.add(new_docent)
    db.commit()
    db.refresh(new_docent)

    return new_docent

@router.get(
    "/{docent_id}",
    summary="Get a docent",
    response_model=DocentResponse
)
async def get_docent(docent_id: int, db: Session = Depends(get_db)):
    # TODO

    docent = db.query(Docent).filter(Docent.id == docent_id).first()

    if docent is None:
        raise HTTPException(status_code=404, detail="Deal Not Found")

    return docent

@router.delete(
    "/{docent_id}",
    summary="Delete a docent",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_docent(docent_id: int, db: Session = Depends(get_db)):
    # TODO
    raise NotImplementedError("TODO")

# Special endpoint: Generate Docent Content
class DocentGenerateInput(BaseModel):
    place_id: int
    tone: str

class DocentGenerateOutput(BaseModel):
    content: str

@router.post(
    "/generate",
    summary="Generate AI docent content",
    response_model=DocentGenerateOutput
)
async def generate_docent(input: DocentGenerateInput):
    """
    Generate docent content based on tone.
    Stub logic: Template based text.
    """
    content = f"당신의 {input.tone} 취향이 이 공간과 맞습니다."
    return {"content": content}
