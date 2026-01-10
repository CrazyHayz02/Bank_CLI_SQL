import psycopg2
from dotenv import load_dotenv
import os
from services.exceptions import DatabaseConnectionError

load_dotenv()

# Database connection settings
DB_NAME = "bank_db"
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        raise DatabaseConnectionError(
            "Failed to connect to the database. "
            "Check DB name, credentials, and whether PostgreSQL is running."
        ) from e