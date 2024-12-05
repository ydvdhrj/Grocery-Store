from .sql_connection import get_sql_connection
import bcrypt
import psycopg2

def create_user(connection, name, email, password):
    cursor = None
    try:
        # Validate input
        if not name or not email or not password:
            return False, "All fields are required"
        
        # Validate email format (basic check)
        if '@' not in email:
            return False, "Invalid email format"
        
        # Validate password strength
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        cursor = connection.cursor()
        
        # Check if user already exists
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        if cursor.fetchone():
            return False, "User with this email already exists"
        
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Insert new user
        query = """INSERT INTO users (name, email, password_hash)
                  VALUES (%s, %s, %s)"""
        cursor.execute(query, (name, email, hashed_password))
        connection.commit()
        
        return True, "User created successfully"
    except psycopg2.Error as e:
        # Specific database-related error handling
        return False, f"Database error: {str(e)}"
    except Exception as e:
        # Catch-all for any other unexpected errors
        return False, f"Unexpected error: {str(e)}"
    finally:
        if cursor:
            cursor.close()

def verify_user(connection, email, password):
    cursor = None
    try:
        # Validate input
        if not email or not password:
            return None, "Email and password are required"
        
        cursor = connection.cursor()
        query = "SELECT id, name, password_hash FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        if not result:
            return None, "User not found"
        
        user_id, name, stored_hash = result
        
        # Convert stored_hash to bytes if it's a string
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return {"id": user_id, "name": name, "email": email}, None
        else:
            return None, "Invalid password"
    except psycopg2.Error as e:
        # Specific database-related error handling
        return None, f"Database error: {str(e)}"
    except Exception as e:
        # Catch-all for any other unexpected errors
        return None, f"Unexpected error: {str(e)}"
    finally:
        if cursor:
            cursor.close()
