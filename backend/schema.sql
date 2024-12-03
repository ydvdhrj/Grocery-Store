-- Create UOM table
CREATE TABLE IF NOT EXISTS uom (
    uom_id SERIAL PRIMARY KEY,
    uom_name VARCHAR(50) NOT NULL
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    uom_id INTEGER REFERENCES uom(uom_id),
    price_per_unit DECIMAL(10, 2) NOT NULL
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order_details table
CREATE TABLE IF NOT EXISTS order_details (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Insert some sample UOM data
INSERT INTO uom (uom_name) VALUES 
    ('kg'),
    ('pieces'),
    ('litre') 
ON CONFLICT DO NOTHING;
