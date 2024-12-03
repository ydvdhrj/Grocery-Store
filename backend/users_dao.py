from .sql_connection import get_sql_connection
import bcrypt
import psycopg2

def create_user(connection, name, email, password):
    try:
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
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()

def verify_user(connection, email, password):
    try:
        cursor = connection.cursor()
        query = "SELECT id, name, password_hash FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        if not result:
            return None, "User not found"
        
        user_id, name, stored_hash = result
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return {"id": user_id, "name": name, "email": email}, None
        else:
            return None, "Invalid password"
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
