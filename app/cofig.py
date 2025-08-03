import os
from dotenv import load_dotenv

load_dotenv()

# Database configurations
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "my_dbms")
}

# PostgreSQL configuration for SQLAlchemy
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)

# MySQL configuration for legacy code
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "my_dbms")
}

# Load .env.test if running tests
if "unittest" in os.environ.get("_", ""):
    load_dotenv(".env.test")
else:
    load_dotenv()
