import os
import sys
import traceback
import psycopg2
from dotenv import load_dotenv

def check_environment_variables():
    print("Checking Environment Variables:")
    # Try loading from .env file first
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    example_env_path = os.path.join(os.path.dirname(__file__), '.env.example')
    
    print(f"Attempting to load .env from: {env_path}")
    print(f"Attempting to load example .env from: {example_env_path}")
    
    # Load .env file if it exists, otherwise load .env.example
    if os.path.exists(env_path):
        load_dotenv(env_path)
    elif os.path.exists(example_env_path):
        load_dotenv(example_env_path)
    else:
        print("WARNING: No .env or .env.example file found!")
    
    required_vars = ['DATABASE_URL', 'SECRET_KEY']
    for var in required_vars:
        value = os.getenv(var)
        print(f"{var}: {'SET' if value else 'NOT SET'}")
        if not value:
            print(f"  Warning: {var} is missing!")

def test_database_connection():
    print("\nTesting Database Connection:")
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            print("ERROR: DATABASE_URL is not set")
            return False
        
        print(f"Attempting to connect to: {DATABASE_URL}")
        
        # Detailed connection parsing
        from urllib.parse import urlparse
        parsed_url = urlparse(DATABASE_URL)
        
        print("Connection Details:")
        print(f"  Scheme: {parsed_url.scheme}")
        print(f"  Hostname: {parsed_url.hostname}")
        print(f"  Path: {parsed_url.path}")
        print(f"  Username: {parsed_url.username}")
        
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Database Version: {db_version[0]}")
        
        # Check users table
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        users_table_exists = cursor.fetchone()[0]
        print(f"Users Table Exists: {users_table_exists}")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Database Connection Error: {e}")
        traceback.print_exc()
        return False

def check_dependencies():
    print("\nChecking Python Dependencies:")
    dependencies = [
        'flask', 'flask_cors', 'flask_login', 
        'psycopg2', 'bcrypt', 'python-dotenv'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"{dep}: INSTALLED")
        except ImportError:
            print(f"{dep}: NOT INSTALLED")

def main():
    print("Server Diagnostic Tool")
    print("=" * 30)
    
    # Add Python and system information
    print(f"Python Version: {sys.version}")
    print(f"Current Working Directory: {os.getcwd()}")
    
    check_environment_variables()
    test_database_connection()
    check_dependencies()

if __name__ == "__main__":
    main()
