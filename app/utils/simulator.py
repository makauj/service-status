import random
from datetime import datetime, timedelta

def simulate_production_dates():
    today = datetime.now()
    days_ago = random.randint(7, 30)
    produced_on = today - timedelta(days=days_ago)

    # Dispatched within 1 to 5 days after production
    dispatched_on = produced_on + timedelta(days=random.randint(1, 5))

    return produced_on.strftime('%Y-%m-%d %H:%M:%S'), dispatched_on.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO users (id_no, name, dob, expires_in, phone_no, image_data) VALUES (?, ?, ?, ?, ?, ?)",
        (id_no, name, dob, expires_in, phone_no, image_data)
    )
    conn.commit()