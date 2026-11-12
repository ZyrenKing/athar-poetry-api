from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional, List
from models import engine
from feature.poems import crud, utils
router = APIRouter(prefix="/poems", tags=["Poems"])

def get_db():
    with Session(engine) as session:
        yield session

# ==========================================
# 1. جلب قائمة القصائد (GET /poems)
# ==========================================
@router.get("/")
def read_poems(
    poet_id: Optional[int] = Query(None, description="فلترة حسب رقم الشاعر"),
    meter_id: Optional[int] = Query(None, description="فلترة حسب رقم البحر"),
    topic_id: Optional[int] = Query(None, description="فلترة حسب رقم الموضوع"),
    skip: int = Query(0, description="عدد القصائد التي سيتم تخطيها"),
    limit: int = Query(10, description="عدد القصائد المطلوبة"),
    db: Session = Depends(get_db)
):
    results, topics_dict = crud.get_poems(
        db=db, 
        poet_id=poet_id, 
        meter_id=meter_id, 
        topic_id=topic_id, 
        skip=skip, 
        limit=limit
    )
    
    # 2. فك التغليف والتنسيق
    formatted_poems = [
        utils.format_poem_list_item(
            poem=row[0], 
            poet_name=row[1], 
            meter_name=row[2], 
            era_name=row[3],
            topics_dict=topics_dict
        )
        for row in results
    ]
    
    return {
        "status": "success",
        "count": len(formatted_poems),
        "skip": skip,
        "limit": limit,
        "data": formatted_poems
    }
# ==========================================
# 2. جلب قصيدة واحدة (GET /poems/{id})
# ==========================================
@router.get("/{poem_id}")
def read_poem(
    poem_id: int,
    db: Session = Depends(get_db)
):
    data = crud.get_poem_by_id(db=db, poem_id=poem_id)
    
    if not data:
        raise HTTPException(status_code=404, detail="القصيدة غير موجودة")
    
    formatted_poem = utils.format_poem_detail(
        poem=data["poem"],
        poet=data["poet"],
        era_name=data["era_name"], 
        meter=data["meter"],
        topics=data["topics"]
    )
    
    return {
        "status": "success",
        "data": formatted_poem
    }