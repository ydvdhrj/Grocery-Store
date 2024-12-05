import requests
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_render_postgres_url(url):
    # Regular expression to parse PostgreSQL connection URL
    pattern = r'postgresql://([^:]+):([^@]+)@([^/]+)/(.+)'
    match = re.match(pattern, url)
    
    if not match:
        print("Invalid PostgreSQL URL format")
        return False
    
    username, password, host, database = match.groups()
    
    print(f"Username: {username}")
    print(f"Host: {host}")
    print(f"Database: {database}")
    
    # Check if host is a Render.com PostgreSQL instance
    if not host.startswith('dpg-'):
        print("Warning: Host does not appear to be a Render.com PostgreSQL instance")
    
    return True

def check_render_database_status(host):
    try:
        # Construct the Render service status URL
        status_url = f"https://dashboard.render.com/service/{host}"
        
        print(f"Checking Render service status for: {host}")
        print("Note: This is a manual check. You'll need to verify in your Render dashboard.")
        print(f"Please visit: {status_url}")
        
    except Exception as e:
        print(f"Error checking database status: {e}")

def main():
    try:
        # Get database URL from environment variable
        DB_URL = os.getenv('DB_URL')
        if not DB_URL:
            raise ValueError("DB_URL environment variable is not set")
            
        print("Validating Database Connection Details:")
        print("-" * 40)
        
        # Validate URL format
        if validate_render_postgres_url(DB_URL):
            print("\nURL Format: Valid")
        else:
            print("\nURL Format: Invalid")
        
        # Extract host for status check
        host_match = re.search(r'@([^/]+)/', DB_URL)
        if host_match:
            host = host_match.group(1)
            check_render_database_status(host)
    except Exception as e:
        print(f"Error validating database URL: {e}")

if __name__ == "__main__":
    main()
