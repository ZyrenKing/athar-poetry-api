from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional

from models import engine
from feature.poets import crud, utils

router = APIRouter(prefix="/poets", tags=["Poets"])

def get_db():
    with Session(engine) as session:
        yield session

# ==========================================
# 1. جلب قائمة الشعراء (GET /poets)
# ==========================================
@router.get("/")
def read_poets(
    search: Optional[str] = Query(None, description="البحث باسم الشاعر"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    results = crud.get_poets(db=db, search=search, skip=skip, limit=limit)
    print(results)
    formatted_poets = [
        utils.format_poet_list_item(poet, era_name, poem_count) 
        for poet, era_name, poem_count in results
    ]
    
    return {
        "status": "success",
        "count": len(formatted_poets),
        "data": formatted_poets
    }

# ==========================================
# 2. جلب تفاصيل شاعر (GET /poets/{id})
# ==========================================
@router.get("/{poet_id}")
def read_poet(
    poet_id: int,
    db: Session = Depends(get_db)
):
    data = crud.get_poet_by_id(db=db, poet_id=poet_id)
    
    if not data:
        raise HTTPException(status_code=404, detail="الشاعر غير موجود")
        
    formatted_poet = utils.format_poet_detail(
        poet=data["poet"],
        era_name=data["era_name"],
        poem_count=data["poem_count"],
        top_meters=data["top_meters"]
    )
    
    return {
        "status": "success",
        "data": formatted_poet
    }

# ==========================================
# 3. جلب قصائد شاعر معين (GET /poets/{id}/poems)
# ==========================================
@router.get("/{poet_id}/poems")
def read_poet_poems(
    poet_id: int,
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    poet = crud.get_poet_by_id(db, poet_id)
    if not poet:
        raise HTTPException(status_code=404, detail="الشاعر غير موجود")
        
    poems = crud.get_poems_by_poet(db=db, poet_id=poet_id, skip=skip, limit=limit)
    
    formatted_poems = [
        utils.format_poet_poem_item(poem, meter_name) 
        for poem, meter_name in poems
    ]
    
    return {
        "status": "success",
        "poet_name": poet["poet"].name,
        "count": len(formatted_poems),
        "data": formatted_poems
    }