import mysql.connector
from app.cofig import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
