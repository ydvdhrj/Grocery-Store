-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    uom_id INT NOT NULL,
    price_per_unit DOUBLE NOT NULL,
    PRIMARY KEY (product_id),
    FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    total DOUBLE NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order details table
CREATE TABLE IF NOT EXISTS order_details (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DOUBLE NOT NULL,
    total_price DOUBLE NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
