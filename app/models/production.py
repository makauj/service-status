from app.db import get_connection
from app.utils.sanitizer import sanitize_id_no

def insert_production(raw_id, expires_on, user_image, produced_on, dispatched_on):
    id_no = sanitize_id_no(raw_id)
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Production (`ID No`, expires_on, user_image, produced_on, dispatched_on)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (id_no, expires_on, user_image, produced_on, dispatched_on))
    conn.commit()

    cursor.close()
    conn.close()
    print("✅ Production record inserted successfully!")

def fetch_production():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Production")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
