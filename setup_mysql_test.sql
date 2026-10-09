-- Create the test database if it does not exist.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user if it does not exist.
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Ensure the required password is set, including for an existing user.
ALTER USER 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant privileges only on the test database.
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant read access only on performance_schema.
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
