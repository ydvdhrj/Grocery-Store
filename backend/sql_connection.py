import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging
import socket
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

__cnx = None

def resolve_hostname(hostname):
    """Attempt to resolve hostname with additional error handling."""
    try:
        # Try standard socket resolution
        ip_address = socket.gethostbyname(hostname)
        logger.info(f"Successfully resolved {hostname} to {ip_address}")
        return True
    except socket.gaierror as e:
        logger.error(f"Hostname resolution failed for {hostname}: {e}")
        
        # Additional DNS troubleshooting
        try:
            # Try alternative resolution methods
            addrinfo = socket.getaddrinfo(hostname, None)
            if addrinfo:
                logger.info(f"Alternative resolution successful for {hostname}")
                return True
        except Exception as alt_e:
            logger.error(f"Alternative resolution failed: {alt_e}")
        
        return False

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
            
            # Extract hostname for resolution check
            parsed_url = urlparse(DATABASE_URL)
            hostname = parsed_url.hostname
            
            # Attempt hostname resolution
            if not resolve_hostname(hostname):
                raise ConnectionError(f"Could not resolve hostname: {hostname}")
            
            logger.info("Establishing new PostgreSQL connection")
            __cnx = psycopg2.connect(
                DATABASE_URL, 
                connect_timeout=10,  # Add connection timeout
                sslmode='require'   # Enforce SSL
            )
            
            # Ensure the connection is in a good state
            __cnx.set_session(autocommit=True)
            
        except Exception as e:
            logger.error(f"Error establishing database connection: {e}")
            # Log detailed error information
            logger.error(f"Connection Error Details: {type(e).__name__}")
            logger.error(f"Error Arguments: {e.args}")
            
            # Provide more context for debugging
            if 'No such host is known' in str(e):
                logger.error("Possible DNS resolution issue. Check your network and database host.")
            
            raise
    
    return __cnx
