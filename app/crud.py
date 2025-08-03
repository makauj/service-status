from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.enhanced_collection import Collection
from app.schemas import CollectionCreate, CollectionUpdate
from datetime import datetime
from typing import List, Optional

def create_collection(db: Session, data: CollectionCreate, read_only: bool, user: str = "system") -> Collection:
    """Create a new collection record with proper business logic"""
    db_entry = Collection(
        id=data.id,
        name=data.name,
        email=data.email,
        contact=data.contact,
        date=data.date or datetime.utcnow().date(),
        read_only=read_only,
        last_updated_by=user,
        last_updated_at=datetime.utcnow()
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_collections(
    db: Session, 
    ID: Optional[int] = None, 
    read_only: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[Collection]:
    """Get collections with optional filtering"""
    query = db.query(Collection)
    
    if ID is not None:
        query = query.filter(Collection.id == ID)
    if read_only is not None:
        query = query.filter(Collection.read_only == read_only)
    
    return query.offset(skip).limit(limit).all()

def get_collection_by_record_id(db: Session, record_id: int) -> Optional[Collection]:
    """Get a specific collection by its record_id"""
    return db.query(Collection).filter(Collection.record_id == record_id).first()

def get_collections_by_id(db: Session, ID: int) -> List[Collection]:
    """Get all collections for a specific ID (for history view)"""
    return db.query(Collection).filter(Collection.id == ID).order_by(Collection.last_updated_at.desc()).all()

def update_collection(db: Session, record_id: int, update_data: CollectionUpdate) -> Optional[Collection]:
    """Update a collection record with read-only enforcement"""
    db_obj = get_collection_by_record_id(db, record_id)
    
    if not db_obj:
        return None
    
    if db_obj.read_only:
        raise ValueError("Cannot update read-only record")
    
    # Update fields
    for field, value in update_data.dict(exclude_unset=True).items():
        if field != 'last_updated_by':  # Handle this separately
            setattr(db_obj, field, value)
    
    # Update audit fields
    db_obj.last_updated_by = update_data.last_updated_by
    db_obj.last_updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_collection(db: Session, record_id: int) -> bool:
    """Delete a collection record"""
    db_obj = get_collection_by_record_id(db, record_id)
    if not db_obj:
        return False
    
    if db_obj.read_only:
        raise ValueError("Cannot delete read-only record")
    
    db.delete(db_obj)
    db.commit()
    return True

def get_editable_collections(db: Session, skip: int = 0, limit: int = 100) -> List[Collection]:
    """Get only editable collections (read_only = False)"""
    return get_collections(db, read_only=False, skip=skip, limit=limit)

def get_readonly_collections(db: Session, skip: int = 0, limit: int = 100) -> List[Collection]:
    """Get only read-only collections"""
    return get_collections(db, read_only=True, skip=skip, limit=limit) 