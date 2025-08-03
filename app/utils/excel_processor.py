import pandas as pd
from datetime import datetime
from typing import List, Tuple, Optional
from app.schemas import CollectionCreate
import logging

logger = logging.getLogger(__name__)

def process_excel_data(file_content: bytes) -> List[Tuple[CollectionCreate, bool]]:
    """
    Process Excel data according to business rules:
    - If 3 columns (ID, Name, Contact) are filled: mark as read_only
    - If only 2 columns filled and one is ID: leave as editable
    - Ignore 'collected' column
    - Email column is ignored during import but can be added later
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_content)
        
        results = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Extract data from Excel row
                id_val = row.get('ID')
                name = row.get('Name')
                contact = row.get('Contact')
                date_val = row.get('Date')
                
                # Skip rows without ID
                if pd.isna(id_val) or id_val is None:
                    continue
                
                # Convert ID to integer
                try:
                    id_val = int(id_val)
                except (ValueError, TypeError):
                    errors.append(f"Row {index + 1}: Invalid ID value '{id_val}'")
                    continue
                
                # Count filled required fields (ID, Name, Contact)
                filled_fields = sum([
                    not pd.isna(id_val),
                    not pd.isna(name) and name is not None and str(name).strip() != '',
                    not pd.isna(contact) and contact is not None and str(contact).strip() != ''
                ])
                
                # Determine read-only status based on business rules
                if filled_fields >= 3:
                    read_only = True
                elif filled_fields == 2 and not pd.isna(id_val):
                    read_only = False
                else:
                    # Skip rows that don't meet minimum requirements
                    continue
                
                # Process date
                if pd.notna(date_val) and date_val is not None:
                    try:
                        if isinstance(date_val, str):
                            date_val = datetime.strptime(date_val, '%Y-%m-%d').date()
                        elif isinstance(date_val, datetime):
                            date_val = date_val.date()
                        else:
                            date_val = datetime.utcnow().date()
                    except (ValueError, TypeError):
                        date_val = datetime.utcnow().date()
                else:
                    date_val = datetime.utcnow().date()
                
                # Create CollectionCreate object
                collection_data = CollectionCreate(
                    ID=id_val,
                    Name=str(name).strip() if pd.notna(name) and name is not None else None,
                    Contact=str(contact).strip() if pd.notna(contact) and contact is not None else None,
                    Date=date_val,
                    Email=None  # Email is ignored during import
                )
                
                results.append((collection_data, read_only))
                
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")
                continue
        
        logger.info(f"Processed {len(results)} valid records from Excel file")
        if errors:
            logger.warning(f"Found {len(errors)} errors during processing")
            
        return results, errors
        
    except Exception as e:
        logger.error(f"Error processing Excel file: {str(e)}")
        raise ValueError(f"Failed to process Excel file: {str(e)}")

def validate_excel_structure(df: pd.DataFrame) -> List[str]:
    """Validate that Excel file has required columns"""
    required_columns = ['ID', 'Name', 'Contact']
    optional_columns = ['Date', 'Collected']
    
    errors = []
    
    # Check for required columns
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")
    
    # Check for unexpected columns
    expected_columns = required_columns + optional_columns
    unexpected_columns = [col for col in df.columns if col not in expected_columns]
    if unexpected_columns:
        errors.append(f"Unexpected columns found: {', '.join(unexpected_columns)}")
    
    return errors 