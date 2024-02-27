-- Set variables
\set user_name '${POSTGRES_USER}'
\set user_password '${POSTGRES_PASSWORD}'
\set db_name '${POSTGRES_DB}'

-- Create user
CREATE USER :user_name WITH PASSWORD :'user_password';
ALTER USER :user_name CREATEDB;

-- Create database
CREATE DATABASE :db_name OWNER :user_name;

-- Connect to the newly created database
\c :db_name;

-- Create table
CREATE TABLE concerts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    artist VARCHAR(255),
    date DATE
);

-- Grant privileges to the user for the database
GRANT ALL PRIVILEGES ON DATABASE :db_name TO :user_name;