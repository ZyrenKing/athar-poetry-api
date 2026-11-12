# poems/crud.py
from sqlmodel import Session, select
from models import Poem, Poet, Meter, Topic, Era
from typing import Optional

def get_poems(
    db: Session, 
    poet_id: Optional[int] = None, 
    meter_id: Optional[int] = None, 
    topic_id: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 10
):
    # 1. بناء الاستعلام الأساسي (بدون أبيات)
    statement = (
        select(Poem, Poet.name, Meter.name, Era.name)
        .join(Poet, Poem.poet_id == Poet.id)
        .join(Meter, Poem.meter_id == Meter.id)
        .join(Era, Poet.era_id == Era.id, isouter=True)
    )
    
    # إضافة الفلاتر
    if poet_id:
        statement = statement.where(Poem.poet_id == poet_id)
    if meter_id:
        statement = statement.where(Poem.meter_id == meter_id)
    if topic_id:
        statement = statement.where(Poem.topic_ids.contains([topic_id]))
        
    statement = statement.offset(skip).limit(limit)
    results = db.exec(statement).all()
    
    # 2. جلب كل الموضوعات كقاموس (ID -> Name) لسرعة الترجمة
    # (هذا الاستعلام خفيف جداً لأن جدول الموضوعات صغير)
    topics_dict = {t.id: t.name for t in db.exec(select(Topic)).all()}
    
    return results, topics_dict


def get_poem_by_id(db: Session, poem_id: int):
    """
    جلب قصيدة واحدة مع كل تفاصيلها (الشاعر، العصر، البحر) في استعلام واحد ذكي
    """
    # 1. استعلام واحد يجلب كل شيء (عدا الموضوعات)
    statement = (
        select(Poem, Poet, Era.name, Meter)
        .join(Poet, Poem.poet_id == Poet.id)
        .join(Era, Poet.era_id == Era.id, isouter=True)
        .join(Meter, Poem.meter_id == Meter.id)
        .where(Poem.id == poem_id)
    )
    
    # نستخدم first() لأننا نريد قصيدة واحدة
    result = db.exec(statement).first()
    print(result)
    if not result:
        return None
        
    # فك التغليف
    poem, poet, era_name, meter = result
    
    # 2. جلب الموضوعات (كما طلبت، بقيت كما هي)
    topics = []
    if poem.topic_ids:
        topics_stmt = select(Topic).where(Topic.id.in_(poem.topic_ids))
        topics = db.exec(topics_stmt).all()
        
    return {
        "poem": poem,
        "poet": poet,
        "era_name": era_name or "غير محدد", # أضفنا العصر هنا
        "meter": meter,
        "topics": topics
    }