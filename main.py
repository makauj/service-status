from app.models.production import insert_production, fetch_production
from app.models.collection import insert_collection, fetch_collections
from app.excel_upload import upload_collection_from_excel
from app.utils.simulator import simulate_production_dates


# Simulate and insert
produced_on, dispatched_on = simulate_production_dates()
insert_production("X990Z", "2026-01-01 00:00:00", dummy_image, produced_on, dispatched_on)


upload_collection_from_excel("collection_data.xlsx")

# Example binary image
dummy_image = b'\x89PNG\r\n\x1a\n...'

# Insert Production record
insert_production("P00A2", "2026-12-31 23:59:59", dummy_image, "2025-07-01 08:00:00", "2025-07-05 15:00:00")

# Fetch Production records
for prod in fetch_production():
    print(prod)

# Insert Collection record
insert_collection("P00A2", "John Doe", "0712345678", "john@example.com")

# Fetch Collection records
for coll in fetch_collections():
    print(coll)
    query = """
        INSERT INTO Users (`ID No`, name, dob, expires_in, phone_no, user_image)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    cursor.execute(query, (id_no, name, dob, expires_in, phone_no, image_data))
    conn.commit()
    
    cursor.close()
    conn.close()
    print("✅ User inserted successfully!")

# Fetch Users records
from app.models.users import insert_user, fetch_users
insert_user("U00A1", "Alice Smith", "1990-01-01", "2025-12-31", "0712345678", dummy_image)
for user in fetch_users():
    print(user)
    print("✅ Collection record inserted successfully!")
    print("✅ Production record inserted successfully!")
    print("✅ User inserted successfully!")
