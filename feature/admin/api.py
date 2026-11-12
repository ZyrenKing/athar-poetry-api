# admin/api.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from pydantic import BaseModel
from models import engine
from feature.admin import crud
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_TOKEN = os.getenv(
    "ADMIN_TOKEN",
)
router = APIRouter(prefix="/admin", tags=["Admin"])

class QueryRequest(BaseModel):
    sql: str

def get_db():
    with Session(engine) as session:
        yield session

@router.post("/query")
def run_custom_query(
    request: QueryRequest,
    x_admin_token: str = Header(default="", description="مفتاح الإدارة السري"),
    db: Session = Depends(get_db)
):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="غير مصرح لك باستخدام هذه الميزة")
    
    forbidden_words = ["drop", "delete", "update", "insert", "alter", "truncate"]
    if any(word in request.sql.lower() for word in forbidden_words):
        raise HTTPException(status_code=400, detail="يُسمح باستعلامات SELECT فقط")
    
    try:
        results = crud.execute_raw_query(db, request.sql)
        return {
            "status": "success",
            "count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"خطأ في الاستعلام: {str(e)}")
