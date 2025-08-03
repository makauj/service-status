from app.db import get_connection
from app.utils.sanitize import sanitize_id_no

def insert_user(raw_id, name, dob, expires_in, phone_no, image_data):
    id_no = sanitize_id_no(raw_id)
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Users (`ID No`, name, dob, expires_in, phone_no, user_image)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (id_no, name, dob, expires_in, phone_no, image_data))
    conn.commit()

    cursor.close()
    conn.close()
    print("✅ User inserted successfully!")

def fetch_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
