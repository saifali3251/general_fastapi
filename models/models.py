from sqlalchemy import Column, String, Integer,DateTime,Text
from db.session import Base
from datetime import datetime


class CachedQuestion(Base):
    __tablename__ = "cached_questions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    type = Column(Text)
    model_name = Column(String)
    cache_key = Column(String, unique=True, index=True)
    response_json = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    hit_count = Column(Integer, default=1)

