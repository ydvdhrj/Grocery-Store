import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

__cnx = None

def get_sql_connection():
    print("Opening PostgreSQL connection")
    global __cnx

    if __cnx is None:
        # Get database URL from environment variable
        DATABASE_URL = os.getenv('DATABASE_URL')
        
        if DATABASE_URL:
            # Render provides DATABASE_URL in the format: postgres://user:password@host:port/dbname
            __cnx = psycopg2.connect(DATABASE_URL)
        else:
            # Local development fallback
            __cnx = psycopg2.connect(
                dbname=os.getenv('DB_NAME', 'grocery_store'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432')
            )
        
    return __cnx
