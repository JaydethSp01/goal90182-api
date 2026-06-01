from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Alerta
from ..schemas import AlertaCreate, AlertaUpdate

router = APIRouter()

@router.get("/alertas", response_model=List[Alerta])
def read_alertas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    alertas = db.query(Alerta).offset(skip).limit(limit).all()
    return alertas

@router.post("/alertas", response_model=Alerta)
def create_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    db_alerta = Alerta(**alerta.dict())
    db.add(db_alerta)
    db.commit()
    db.refresh(db_alerta)
    return db_alerta

@router.put("/alertas/{alerta_id}", response_model=Alerta)
def update_alerta(alerta_id: int, alerta: AlertaUpdate, db: Session = Depends(get_db)):
    db_alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    for key, value in alerta.dict().items():
        setattr(db_alerta, key, value)
    db.commit()
    db.refresh(db_alerta)
    return db_alerta

@router.delete("/alertas/{alerta_id}")
def delete_alerta(alerta_id: int, db: Session = Depends(get_db)):
    db_alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    db.delete(db_alerta)
    db.commit()
    return {"message": "Alerta eliminada"}
