# statistics/crud.py
from sqlmodel import Session, select, func
from models import Poem, Poet, Era, Meter

def get_era_statistics(db: Session):
    """عدد القصائد في كل عصر"""
    statement = (
        select(Era.name, func.count(Poem.id).label("count"))
        .join(Poet, Poet.era_id == Era.id)
        .join(Poem, Poem.poet_id == Poet.id)
        .group_by(Era.name)
        .order_by(func.count(Poem.id).desc())
    )
    return db.exec(statement).all()

def get_meter_statistics(db: Session):
    """عدد القصائد على كل بحر"""
    statement = (
        select(Meter.name, func.count(Poem.id).label("count"))
        .join(Poem, Poem.meter_id == Meter.id)
        .group_by(Meter.name)
        .order_by(func.count(Poem.id).desc())
    )
    return db.exec(statement).all()

def get_top_poets(db: Session, limit: int = 10):
    """أكثر الشعراء إنتاجاً للقصائد"""
    statement = (
        select(Poet.name, func.count(Poem.id).label("count"))
        .join(Poem, Poem.poet_id == Poet.id)
        .group_by(Poet.name)
        .order_by(func.count(Poem.id).desc())
        .limit(limit)
    )
    return db.exec(statement).all()