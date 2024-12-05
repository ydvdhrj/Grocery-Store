import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise ValueError("DB_URL environment variable is not set")

def create_users_table():
    try:
        # Establish connection
        connection = psycopg2.connect(DB_URL)
        
        # Create a cursor
        cursor = connection.cursor()
        
        # SQL to create users table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        );
        """
        
        # Execute the query
        cursor.execute(create_table_query)
        
        # Commit the changes
        connection.commit()
        
        print("Users table created successfully!")
    
    except psycopg2.Error as e:
        print(f"Error creating users table: {e}")
    
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    create_users_table()
