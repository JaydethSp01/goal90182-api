from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Stock
from ..schemas import StockCreate, StockUpdate

router = APIRouter()

@router.get("/stocks", response_model=List[Stock])
def read_stocks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stocks = db.query(Stock).offset(skip).limit(limit).all()
    return stocks

@router.post("/stocks", response_model=Stock)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    db_stock = Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@router.put("/stocks/{stock_id}", response_model=Stock)
def update_stock(stock_id: int, stock: StockUpdate, db: Session = Depends(get_db)):
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    for key, value in stock.dict().items():
        setattr(db_stock, key, value)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@router.delete("/stocks/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    db.delete(db_stock)
    db.commit()
    return {"message": "Stock eliminado"}
