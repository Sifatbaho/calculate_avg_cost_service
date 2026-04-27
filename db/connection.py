import psycopg2
from psycopg2.extras import RealDictCursor


from decouple import config

DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

print(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

def _get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def get_cursor():
    conn = _get_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)
