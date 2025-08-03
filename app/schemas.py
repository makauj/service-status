from pydantic import BaseModel
from typing import Optional, Union
from datetime import date, datetime

class CollectionBase(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None
    date: Optional[Union[date, datetime]] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None
    date: Optional[Union[date, datetime]] = None
    last_updated_by: str

class CollectionOut(CollectionBase):
    record_id: int
    read_only: bool
    last_updated_by: Optional[str] = None
    last_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CollectionHistory(BaseModel):
    id: int
    collections: list[CollectionOut]

class ExcelUploadResponse(BaseModel):
    message: str
    records_processed: int
    records_added: int
    errors: list[str] = [] 