import psycopg2
import socket
import ssl

def test_database_connection():
    # Database connection details
    db_url = "postgresql://grocery_store_18ec_user:JhC7r8dc959vtGdUprCEJPatiMIDdrHu@dpg-ct7apsbtq21c73blhkm0-a/grocery_store_18ec"
    
    try:
        # Extract host from the connection string
        host = "dpg-ct7apsbtq21c73blhkm0-a"
        
        # Test DNS resolution
        print("Resolving host...")
        socket.gethostbyname(host)
        print("DNS resolution successful")
        
        # Test SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Attempt to establish connection
        print("Attempting to connect to database...")
        connection = psycopg2.connect(
            db_url,
            sslcontext=ssl_context,
            connect_timeout=10
        )
        
        # Create a cursor and execute a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        print("Database connection successful!")
        print("Test query result:", result)
        
        # Close cursor and connection
        cursor.close()
        connection.close()
        
    except socket.gaierror as e:
        print(f"DNS Resolution Error: {e}")
    except psycopg2.Error as e:
        print(f"Database Connection Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    test_database_connection()
