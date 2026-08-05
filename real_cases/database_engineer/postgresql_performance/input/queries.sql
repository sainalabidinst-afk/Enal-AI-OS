-- Queries to optimize
SELECT * FROM orders WHERE user_id = 123;
SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at;
SELECT u.name, COUNT(o.id) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name;
