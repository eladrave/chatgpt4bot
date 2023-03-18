CREATE DATABASE your_database_name;

\c your_database_name

CREATE TABLE chat (
    ID SERIAL PRIMARY KEY,
    DateTime TIMESTAMP NOT NULL,
    "From" VARCHAR(20) NOT NULL,
    "To" VARCHAR(20) NOT NULL,
    Role TEXT CHECK (Role IN ('system', 'user', 'assistant')) NOT NULL,
    Message TEXT NOT NULL
);
