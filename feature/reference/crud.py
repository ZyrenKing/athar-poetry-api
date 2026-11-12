from sqlmodel import Session, select
from models import Topic, Meter, Era

def get_all_topics(db: Session):
    """جلب كل الموضوعات"""
    return db.exec(select(Topic)).all()

def get_all_meters(db: Session):
    """جلب كل البحور"""
    return db.exec(select(Meter)).all()

def get_all_eras(db: Session):
    """جلب كل العصور"""
    return db.exec(select(Era)).all()