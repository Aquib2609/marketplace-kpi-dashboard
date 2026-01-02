SELECT COUNT(*) AS total_users
FROM users;

SELECT DATE(signup_date) AS date,
       COUNT(*) AS new_users
FROM users
GROUP BY DATE(signup_date)
ORDER BY date;

SELECT DATE_TRUNC('month', signup_d) AS month,
       COUNT(*) AS new_users
FROM users
GROUP BY month
ORDER BY month;






