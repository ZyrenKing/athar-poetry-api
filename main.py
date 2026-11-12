from fastapi import FastAPI, HTTPException, Request
import time
from datetime import datetime
from feature.poems.api import router as poems_router
from feature.poets.api import router as poets_router
from feature.reference.api import router as reference_router 
from feature.statistics.api import router as stats_router 
from feature.admin.api import router as admin_router
import uvicorn
import os
import json

app = FastAPI(title="Athar Poetry API")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 1. بدء المؤقت (بدقة عالية جداً)
    start_time = time.perf_counter()
    
    # 2. تمرير الطلب للسيرفر (هنا يتم تنفيذ كود الـ API)
    response = await call_next(request)
    
    # 3. إيقاف المؤقت وحساب الفرق
    process_time_ms = (time.perf_counter() - start_time) * 1000
    
    # 4. إضافة الوقت في ترويسة الرد (ليراه أي مبرمج عميل)
    response.headers["X-Process-Time"] = f"{process_time_ms:.2f} ms"
    
    # 5. طباعة الوقت في ترمنال السيرفر (لمراقبة الأداء بنفسك)
    print(f"⏱️ {request.method} {request.url.path} -> {process_time_ms:.2f} ms")
    
    return response

app.include_router(poems_router)
app.include_router(poets_router)
app.include_router(reference_router)
app.include_router(stats_router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {
        "message": "Athar Poetry API is running.",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/help", tags=["Documentation"])
def get_api_documentation():
    """يرجع دليلاً شاملاً لكل مسارات الـ API بالتفصيل"""
    file_path = "doc.json"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="ملف التوثيق doc.json غير موجود")
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            doc_data = json.load(f)
        return doc_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء قراءة ملف التوثيق: {str(e)}")
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)