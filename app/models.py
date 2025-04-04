from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl

class URLItem(BaseModel):
    target_url: HttpUrl
    custom_code: Optional[str]=None

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(20), unique=True, index=True, nullable=False)
    target_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)
