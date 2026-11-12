from sqlmodel import Session, text

def execute_raw_query(db: Session, sql_query: str):
    """تنفيذ استعلام SQL خام"""
    result = db.exec(text(sql_query))
    return [dict(row._mapping) for row in result.all()]