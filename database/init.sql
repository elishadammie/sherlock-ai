-- Create Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT,
    signup_date TEXT
);

-- Create Products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL
);

-- Create Sales table
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);

-- Seed Customers
INSERT INTO customers (name, region, signup_date) VALUES
('Alice Johnson', 'North', '2023-01-15'),
('Bob Smith', 'South', '2023-02-20'),
('Carol Davis', 'East', '2023-03-05');

-- Seed Products
INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Phone', 'Electronics', 599.49),
('Desk Chair', 'Furniture', 129.99);

-- Seed Sales
INSERT INTO sales (customer_id, product_id, quantity, sale_date) VALUES
(1, 1, 1, '2023-04-10'),
(2, 2, 2, '2023-04-12'),
(3, 3, 1, '2023-04-15');
