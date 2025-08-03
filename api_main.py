from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.database import get_db, engine
from app.models.enhanced_collection import Base
from app.crud import (
    create_collection, get_collections, get_collection_by_record_id,
    update_collection, delete_collection, get_collections_by_id,
    get_editable_collections, get_readonly_collections
)
from app.schemas import (
    CollectionCreate, CollectionUpdate, CollectionOut, 
    CollectionHistory, ExcelUploadResponse
)
from app.utils.excel_processor import process_excel_data

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Collection Management API",
    description="API for managing collections with Excel upload and read-only enforcement",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for getting current user (simplified)
def get_current_user(x_user: str = Header(None, alias="X-User")):
    if not x_user:
        raise HTTPException(status_code=401, detail="Missing X-User header")
    return x_user

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Collection Management API", "version": "1.0.0"}

@app.post("/upload/", response_model=ExcelUploadResponse)
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Upload Excel file and process collections according to business rules
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Process Excel data
        results, errors = process_excel_data(file_content)
        
        # Insert records into database
        records_added = 0
        for collection_data, read_only in results:
            try:
                create_collection(db, collection_data, read_only, current_user)
                records_added += 1
            except Exception as e:
                errors.append(f"Failed to insert record: {str(e)}")
        
        return ExcelUploadResponse(
            message="Excel file processed successfully",
            records_processed=len(results),
            records_added=records_added,
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.get("/collections/", response_model=List[CollectionOut])
async def read_collections(
    ID: Optional[int] = Query(None, description="Filter by ID"),
    read_only: Optional[bool] = Query(None, description="Filter by read-only status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get collections with optional filtering
    """
    collections = get_collections(db, ID=ID, read_only=read_only, skip=skip, limit=limit)
    return collections

@app.get("/collections/editable/", response_model=List[CollectionOut])
async def read_editable_collections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get only editable collections (read_only = False)
    """
    collections = get_editable_collections(db, skip=skip, limit=limit)
    return collections

@app.get("/collections/readonly/", response_model=List[CollectionOut])
async def read_readonly_collections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get only read-only collections
    """
    collections = get_readonly_collections(db, skip=skip, limit=limit)
    return collections

@app.get("/collections/{record_id}", response_model=CollectionOut)
async def read_collection(record_id: int, db: Session = Depends(get_db)):
    """
    Get a specific collection by record_id
    """
    collection = get_collection_by_record_id(db, record_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@app.get("/collections/history/{ID}", response_model=CollectionHistory)
async def read_collection_history(ID: int, db: Session = Depends(get_db)):
    """
    Get all collections for a specific ID (history view)
    """
    collections = get_collections_by_id(db, ID)
    if not collections:
        raise HTTPException(status_code=404, detail=f"No collections found for ID {ID}")
    
    return CollectionHistory(ID=ID, collections=collections)

@app.put("/collections/{record_id}", response_model=CollectionOut)
async def update_collection_record(
    record_id: int,
    update_data: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Update a collection record (only if not read-only)
    """
    try:
        # Set the current user as the updater
        update_data.last_updated_by = current_user
        
        collection = update_collection(db, record_id, update_data)
        if collection is None:
            raise HTTPException(status_code=404, detail="Collection not found")
        return collection
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.delete("/collections/{record_id}")
async def delete_collection_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Delete a collection record (only if not read-only)
    """
    try:
        success = delete_collection(db, record_id)
        if not success:
            raise HTTPException(status_code=404, detail="Collection not found")
        return {"message": "Collection deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 