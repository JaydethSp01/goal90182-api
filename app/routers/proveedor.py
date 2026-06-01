from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Proveedor
from ..schemas import ProveedorCreate, ProveedorUpdate

router = APIRouter()

@router.get("/proveedores", response_model=List[Proveedor])
def read_proveedores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    proveedores = db.query(Proveedor).offset(skip).limit(limit).all()
    return proveedores

@router.post("/proveedores", response_model=Proveedor)
def create_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    db_proveedor = Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.put("/proveedores/{proveedor_id}", response_model=Proveedor)
def update_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, db: Session = Depends(get_db)):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for key, value in proveedor.dict().items():
        setattr(db_proveedor, key, value)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.delete("/proveedores/{proveedor_id}")
def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(db_proveedor)
    db.commit()
    return {"message": "Proveedor eliminado"}
