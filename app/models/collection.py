from app.db import get_connection
from app.utils.sanitize import sanitize_id_no
from datetime import datetime

def insert_collection(raw_id, collected_by, phone_no, email_address=None):
    id_no = sanitize_id_no(raw_id)
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Collection (`ID No`, collected_by, phone_no, email_address, collection_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    collection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(query, (id_no, collected_by, phone_no, email_address, collection_date))
    conn.commit()

    cursor.close()
    conn.close()
    print("✅ Collection record inserted successfully!")

def fetch_collections():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Collection")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
