-- PostgreSQL Performance Analysis Case
-- Database: E-commerce orders table with performance issues

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total DECIMAL(10,2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Missing index on frequently queried columns
SELECT * FROM orders WHERE user_id = 123;
SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at;

-- N+1 query pattern in application
SELECT * FROM orders WHERE user_id = 123;
SELECT * FROM order_items WHERE order_id = 1;
SELECT * FROM order_items WHERE order_id = 2;
-- ... repeated for each order
