-- Create the test database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant access to the test database
GRANT ALL PRIVILEGES ON hbnb_test_db.*
TO 'hbnb_test'@'localhost';

FLUSH PRIVILEGES;
