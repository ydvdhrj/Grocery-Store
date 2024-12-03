from backend.sql_connection import get_sql_connection
import psycopg2

def create_users_table():
    try:
        # Establish connection
        connection = get_sql_connection()
        
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

if __name__ == "__main__":
    create_users_table()
