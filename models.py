from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import ARRAY
import os
DB_URL = os.getenv(
    "DATABASE_URL",
)
class Era(SQLModel, table=True):
    __tablename__ = "eras"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

class Meter(SQLModel, table=True):
    __tablename__ = "meters"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

class Topic(SQLModel, table=True):
    __tablename__ = "topics"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

class Poet(SQLModel, table=True):
    __tablename__ = "poets"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    era_id: Optional[int] = Field(default=None, foreign_key="eras.id", index=True)

class Poem(SQLModel, table=True):
    __tablename__ = "poems"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    
    url: str = Field(index=True)
    title: str
    poet_id: int = Field(foreign_key="poets.id", index=True)
    meter_id: int = Field(foreign_key="meters.id", index=True)
    
    topic_ids: List[int] = Field(default_factory=list, sa_column=Column(ARRAY(Integer)))
    verses: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(Text)))
    
    verse_count: int
    content_hash: Optional[str] = Field(default=None, unique=True, index=True) 

engine = create_engine(DB_URL,
    pool_size=20,        
    max_overflow=80,    
    pool_timeout=30,    
    pool_pre_ping=True  
)
def create_db_and_tables():
    print("جاري الاتصال بقاعدة البيانات وإنشاء الجداول...")
    SQLModel.metadata.create_all(engine)
    print("✅ ممتاز! تم إنشاء الجداول الخمسة بنجاح.")

if __name__ == "__main__":
    create_db_and_tables()