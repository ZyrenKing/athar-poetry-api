from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import engine
from feature.reference import crud, utils

router = APIRouter(tags=["Reference"])

def get_db():
    with Session(engine) as session:
        yield session

# ==========================================
# 1. جلب كل الموضوعات (GET /topics)
# ==========================================
@router.get("/topics")
def read_topics(db: Session = Depends(get_db)):
    topics = crud.get_all_topics(db)
    formatted_topics = [utils.format_reference_item(t) for t in topics]
    
    return {
        "status": "success",
        "count": len(formatted_topics),
        "data": formatted_topics
    }

# ==========================================
# 2. جلب كل البحور (GET /meters)
# ==========================================
@router.get("/meters")
def read_meters(db: Session = Depends(get_db)):
    meters = crud.get_all_meters(db)
    formatted_meters = [utils.format_reference_item(m) for m in meters]
    
    return {
        "status": "success",
        "count": len(formatted_meters),
        "data": formatted_meters
    }

# ==========================================
# 3. جلب كل العصور (GET /eras)
# ==========================================
@router.get("/eras")
def read_eras(db: Session = Depends(get_db)):
    eras = crud.get_all_eras(db)
    formatted_eras = [utils.format_reference_item(e) for e in eras]
    
    return {
        "status": "success",
        "count": len(formatted_eras),
        "data": formatted_eras
    }