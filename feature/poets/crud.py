from sqlmodel import Session, select, func
from models import Poet, Era, Poem, Meter
from typing import Optional

def get_poets(db: Session, search: Optional[str] = None, skip: int = 0, limit: int = 10):
    """جلب الشعراء مع إمكانية البحث بالاسم + عدد الأشعار"""
    
    statement = (
        select(Poet, Era.name, func.count(Poem.id).label("poem_count"))
        .join(Era, Poet.era_id == Era.id, isouter=True)
        .join(Poem, Poem.poet_id == Poet.id, isouter=True)
        .group_by(Poet.id, Era.name)
    )
    
    if search:
        statement = statement.where(Poet.name.ilike(f"%{search}%"))
        
    statement = statement.offset(skip).limit(limit)
    return db.exec(statement).all()

def get_poet_by_id(db: Session, poet_id: int):
    """جلب تفاصيل الشاعر مع إحصاءات"""
    statement = (
        select(Poet, Era.name)
        .join(Era, Poet.era_id == Era.id, isouter=True)
        .where(Poet.id == poet_id)
    )
    
    result = db.exec(statement).first()
    poet, era_name = result

    if not result:
        return None

    if not era_name:
        era_name = "غير محدد"
    
    count_stmt = select(func.count(Poem.id)).where(Poem.poet_id == poet_id)
    poem_count = db.exec(count_stmt).one()
    
    meters_stmt = (
        select(Meter.name, func.count(Poem.id))
        .join(Poem, Poem.meter_id == Meter.id)
        .where(Poem.poet_id == poet_id)
        .group_by(Meter.name)
        .order_by(func.count(Poem.id).desc())
        .limit(5)
    )
    top_meters_results = db.exec(meters_stmt).all()
    top_meters = [{"meter": m[0], "poem_count": m[1]} for m in top_meters_results]

    return {
        "poet": poet,
        "era_name": era_name,
        "poem_count": poem_count,
        "top_meters": top_meters
    }

def get_poems_by_poet(db: Session, poet_id: int, skip: int = 0, limit: int = 10):
    """جلب قصائد شاعر معين مع اسم البحر"""
    statement = (
        select(Poem, Meter.name)
        .join(Meter, Poem.meter_id == Meter.id)
        .where(Poem.poet_id == poet_id)
        .offset(skip)
        .limit(limit)
    )
    return db.exec(statement).all()