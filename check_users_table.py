import os
import psycopg2
import socket
import ssl
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_users_table():
    try:
        # Get database URL from environment variable
        DB_URL = os.getenv('DB_URL')
        if not DB_URL:
            raise ValueError("DB_URL environment variable is not set")
        
        # Parse the URL
        url_parts = urlparse(DB_URL)
        
        # Attempt to resolve hostname using socket
        print(f"Attempting to resolve: {url_parts.hostname}")
        try:
            # Try to get IP address
            ip_address = socket.gethostbyname(url_parts.hostname)
            print(f"Resolved IP: {ip_address}")
        except socket.gaierror as dns_error:
            print(f"DNS Resolution Error: {dns_error}")
            
            # Alternative connection attempt
            connection_params = {
                'host': url_parts.hostname,
                'database': url_parts.path.strip('/'),
                'user': url_parts.username,
                'password': url_parts.password,
                'port': url_parts.port or 5432
            }
            
            print("Attempting direct connection with parsed parameters")
            connection = psycopg2.connect(**connection_params, sslmode='require')
            cursor = connection.cursor()
        else:
            # Create SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Establish connection
            connection = psycopg2.connect(
                DB_URL,
                sslcontext=ssl_context,
                connect_timeout=10
            )
            cursor = connection.cursor()
        
        # Query to check if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        
        # Fetch the result
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("Users table exists!")
            
            # Get table structure
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users';
            """)
            columns = cursor.fetchall()
            
            print("\nTable Structure:")
            for column in columns:
                print(f"Column: {column[0]}, Type: {column[1]}")
            
            # Count number of rows
            cursor.execute("SELECT COUNT(*) FROM users;")
            row_count = cursor.fetchone()[0]
            print(f"\nNumber of rows in users table: {row_count}")
        else:
            print("Users table does not exist!")
        
    except psycopg2.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    check_users_table()
