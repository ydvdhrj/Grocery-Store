import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL
db_url = os.getenv('DB_URL')

# Connect to the database
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

# Create tables
try:
    # Create UOM table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS uom (
        uom_id SERIAL PRIMARY KEY,
        uom_name VARCHAR(20) NOT NULL
    )
    ''')

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash BYTEA NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        uom_id INT NOT NULL,
        price_per_unit DOUBLE PRECISION NOT NULL,
        FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
    )
    ''')

    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        total DOUBLE PRECISION NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create Order Details table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_details (
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity DOUBLE PRECISION NOT NULL,
        total_price DOUBLE PRECISION NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')

    # Insert some basic UOM values
    cursor.execute('''
    INSERT INTO uom (uom_name) 
    VALUES ('kg'), ('liters'), ('pieces')
    ON CONFLICT DO NOTHING
    ''')

    conn.commit()
    print("All tables created successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
