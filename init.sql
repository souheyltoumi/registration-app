-- Create the database
CREATE DATABASE my_database;

-- Create a new user
-- CREATE USER register_user
-- WITH ENCRYPTED PASSWORD 'register_user';

-- Grant privileges to the user for the database
GRANT ALL PRIVILEGES ON DATABASE register_db TO register_user;

-- Connect to the database
\c register_db;

-- Create the 'tokens' table
CREATE TABLE tokens
(
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) NOT NULL,
    creation_timestamp TIMESTAMP
);

-- Create the 'users' table
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    token_id INT REFERENCES tokens(id),
    active BOOLEAN
);