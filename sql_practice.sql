SELECT * FROM users;

SELECT * FROM users WHERE id = 5;

SELECT * FROM users WHERE name ILIKE '%a%';

SELECT * FROM users WHERE email = 'gojo@gmail.com';

SELECT * FROM users OFFSET 0 LIMIT 10;

SELECT * FROM users OFFSET 10 LIMIT 10;

SELECT * FROM users ORDER BY age ASC;

SELECT * FROM users ORDER BY age DESC;

SELECT * FROM users ORDER BY name ASC;

SELECT * FROM users WHERE age > 20;

SELECT * FROM users WHERE age BETWEEN 19 AND 25;

SELECT COUNT(*) FROM users;

SELECT COUNT(*) FROM users WHERE org_id = 1;

SELECT AVG(age) FROM users;

SELECT MIN(age), MAX(age) FROM users;

SELECT org_id, COUNT(*) FROM users GROUP BY org_id;

SELECT users.id, users.name, users.email, organizations.name AS org_name
FROM users
LEFT JOIN organizations ON users.org_id = organizations.id;

SELECT users.name, users.email, organizations.name AS org_name
FROM users
LEFT JOIN organizations ON users.org_id = organizations.id
WHERE organizations.name = 'Survey Corps';

SELECT organizations.name, COUNT(users.id) AS member_count
FROM organizations
LEFT JOIN users ON organizations.id = users.org_id
GROUP BY organizations.name;

EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'gojo@gmail.com';

EXPLAIN ANALYZE SELECT * FROM users WHERE name ILIKE '%a%';