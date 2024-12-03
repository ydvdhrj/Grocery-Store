import os
import psycopg2

# Set the database URL
DATABASE_URL = 'postgresql://grocery_store_18ec_user:JhC7r8dc959vtGdUprCEJPatiMIDdrHu@dpg-ct7apsbtq21c73blhkm0-a/grocery_store_18ec'

def create_users_table():
    try:
        # Establish connection
        connection = psycopg2.connect(DATABASE_URL)
        
        # Create a cursor
        cursor = connection.cursor()
        
        # SQL to create users table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
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
