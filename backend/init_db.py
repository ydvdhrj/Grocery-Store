import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def init_db():
    # Get database URL from environment variable
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable is not set")
    
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    try:
        print("Creating tables...")
        # Read schema.sql file from the same directory as this script
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        # Execute schema
        cur.execute(schema)
        
        # Commit the changes
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_db()
