from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.models import FactCheck
from app.schemas.schemas import FactCheckCreate, FactCheckResponse
from typing import List

router = APIRouter(prefix="/api/fact-checks", tags=["Fact Checks"])

@router.get("/", response_model=List[FactCheckResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(FactCheck).filter(FactCheck.is_active == True).all()

@router.get("/{fact_check_id}", response_model=FactCheckResponse)
def get_one(fact_check_id: int, db: Session = Depends(get_db)):
    fc = db.query(FactCheck).filter(FactCheck.id == fact_check_id).first()
    if not fc:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    return fc

@router.post("/", response_model=FactCheckResponse, status_code=201)
def create(fc: FactCheckCreate, db: Session = Depends(get_db)):
    db_fc = FactCheck(**fc.model_dump())
    db.add(db_fc)
    db.commit()
    db.refresh(db_fc)
    return db_fc
