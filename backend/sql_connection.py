import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

__cnx = None

def get_sql_connection():
    global __cnx
    
    # Always try to get a fresh connection
    if __cnx is not None:
        try:
            # Check if the connection is still valid
            with __cnx.cursor() as cur:
                cur.execute("SELECT 1")
        except (psycopg2.Error, psycopg2.OperationalError):
            __cnx = None
    
    # If no valid connection, create a new one
    if __cnx is None:
        try:
            # Get database URL from environment variable
            DATABASE_URL = os.getenv('DATABASE_URL')
            
            if not DATABASE_URL:
                raise ValueError("DATABASE_URL environment variable is not set")
            
            logger.info("Establishing new PostgreSQL connection")
            __cnx = psycopg2.connect(DATABASE_URL)
            
            # Ensure the connection is in a good state
            __cnx.set_session(autocommit=True)
            
        except Exception as e:
            logger.error(f"Error establishing database connection: {e}")
            raise
    
    return __cnx
