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
    try:
        # Get database URL from environment variable
        DB_URL = os.getenv('DB_URL')
        logger.info(f"Database URL: {DB_URL}")
        if not DB_URL:
            raise ValueError("DB_URL environment variable is not set")

        # Establish a new PostgreSQL connection
        logger.info("Establishing new PostgreSQL connection")
        connection = psycopg2.connect(
            DB_URL,
            connect_timeout=10,  # Add connection timeout
            sslmode='require'   # Enforce SSL
        )
        return connection
    except Exception as e:
        logger.error(f"Error establishing database connection: {e}")
        raise
