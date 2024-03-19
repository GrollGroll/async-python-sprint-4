from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from .base import Base

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(String, primary_key = True)
    original_url = Column(String, unique=True, nullable=False)
    shortened_url = Column(String, unique=True, nullable=False)
    num_of_visit = Column(Integer)
    created_at = Column(DateTime, index=True, default=datetime.now)