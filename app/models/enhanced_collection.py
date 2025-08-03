from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class Collection(Base):
    __tablename__ = 'collections'
    
    record_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, nullable=False, index=True)  # Foreign key to other tables
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    contact = Column(String(255), nullable=True)
    date = Column(Date, default=datetime.utcnow)
    read_only = Column(Boolean, default=False)
    last_updated_by = Column(String(255), nullable=True)
    last_updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Collection(record_id={self.record_id}, id={self.id}, name='{self.name}', read_only={self.read_only})>" 