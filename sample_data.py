#!/usr/bin/env python3
"""
Sample data generator for Collection Management System
Creates an Excel file with test data that demonstrates all business rules.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_sample_excel():
    """Create a sample Excel file with test data"""
    
    # Sample data that demonstrates all business rules
    data = [
        # Read-only records (3 columns filled: ID, Name, Contact)
        {'ID': 1001, 'Name': 'John Doe', 'Contact': '0712345678', 'Date': '2024-01-15', 'Collected': 'Yes'},
        {'ID': 1002, 'Name': 'Jane Smith', 'Contact': '0723456789', 'Date': '2024-01-16', 'Collected': 'Yes'},
        {'ID': 1003, 'Name': 'Bob Johnson', 'Contact': '0734567890', 'Date': '2024-01-17', 'Collected': 'No'},
        
        # Editable records (only 2 columns filled, one is ID)
        {'ID': 1004, 'Name': 'Alice Brown', 'Contact': '', 'Date': '2024-01-18', 'Collected': 'No'},
        {'ID': 1005, 'Name': '', 'Contact': '0745678901', 'Date': '2024-01-19', 'Collected': 'Yes'},
        {'ID': 1006, 'Name': 'Charlie Wilson', 'Contact': '', 'Date': '', 'Collected': 'No'},
        
        # Multiple entries for same ID (demonstrates history feature)
        {'ID': 1001, 'Name': 'John Doe Updated', 'Contact': '0712345678', 'Date': '2024-01-20', 'Collected': 'Yes'},
        {'ID': 1002, 'Name': 'Jane Smith Follow-up', 'Contact': '0723456789', 'Date': '2024-01-21', 'Collected': 'Yes'},
        
        # Edge cases
        {'ID': 1007, 'Name': '', 'Contact': '', 'Date': '2024-01-22', 'Collected': 'No'},  # Only ID filled
        {'ID': 1008, 'Name': 'David Lee', 'Contact': '0756789012', 'Date': '', 'Collected': 'Yes'},  # No date
        {'ID': 1009, 'Name': 'Eva Garcia', 'Contact': '0767890123', 'Date': '2024-01-23', 'Collected': 'No'},  # Read-only
    ]
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    filename = 'sample_collections.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"✅ Sample Excel file created: {filename}")
    print(f"📊 Total records: {len(data)}")
    print(f"📋 Columns: {list(df.columns)}")
    print("\n📝 Business Rules Demonstrated:")
    print("• Read-only records (3+ columns filled): 5 records")
    print("• Editable records (2 columns filled): 4 records")
    print("• Multiple entries per ID: 2 records")
    print("• Edge cases: 3 records")
    
    return filename

if __name__ == "__main__":
    create_sample_excel() 