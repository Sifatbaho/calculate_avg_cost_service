import psycopg2
from psycopg2.extras import RealDictCursor

def _get_connection():
    return psycopg2.connect(
        dbname="your_db",
        user="postgres",
        password="password",
        host="localhost",
        port=5432
    )

def get_cursor():
    conn = _get_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)
