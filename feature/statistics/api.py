from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from models import engine
from feature.statistics import crud, utils 
router = APIRouter(prefix="/stats", tags=["Statistics"])

def get_db():
    with Session(engine) as session:
        yield session

@router.get("/eras")
def read_era_stats(db: Session = Depends(get_db)):
    results = crud.get_era_statistics(db)
    data = [utils.format_stat_item(row[0], row[1]) for row in results]
    return {"status": "success", "data": data}

@router.get("/meters")
def read_meter_stats(db: Session = Depends(get_db)):
    results = crud.get_meter_statistics(db)
    data = [utils.format_stat_item(row[0], row[1]) for row in results]
    return {"status": "success", "data": data}

@router.get("/top-poets")
def read_top_poets(limit: int = Query(10, description="عدد الشعراء المطلوبين"), db: Session = Depends(get_db)):
    results = crud.get_top_poets(db, limit)
    data = [utils.format_stat_item(row[0], row[1]) for row in results]
    return {"status": "success", "data": data}