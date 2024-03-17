from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from .base import Base

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key = True)
    original_url = Column(String, unique=True, nullable=False)
    shortened_url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now)