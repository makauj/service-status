import pandas as pd
from app.models.collection import insert_collection
from app.db import get_connection

def upload_collection_with_manual_input(file_path):
    try:
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            raw_id = str(row['ID No']).strip()

            print(f"\n🔹 Enter collection info for ID No: {raw_id}")
            collected_by = input("  - Collected by: ").strip()
            phone_no = input("  - Phone number: ").strip()
            email_address = input("  - Email (optional): ").strip()

            if email_address == "":
                email_address = None

            insert_collection(raw_id, collected_by, phone_no, email_address)

        print("\n✅ Collection entries uploaded successfully.")

    except Exception as e:
        print("❌ Error processing Excel file:", e)
    cursor = conn.cursor()
    conn = get_connection()

def upload_collection_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            raw_id = str(row['ID No']).strip()
            collected_by = str(row['Collected By']).strip()
            phone_no = str(row['Phone No']).strip()
            email_address = str(row.get('Email Address', '')).strip() or None

            insert_collection(raw_id, collected_by, phone_no, email_address)

        print("\n✅ Collection entries uploaded successfully.")

    except Exception as e:
        print("❌ Error processing Excel file:", e)
        cursor.close()
        conn.close()
        print("❌ Database connection closed due to error.")
        raise e
    finally:
        cursor.close()
        conn.close()
        print("✅ Database connection closed successfully.")
        cursor = conn.cursor()
        conn = get_connection()
        print("✅ Collection entries uploaded successfully.")
        cursor.close()
        conn.close()
