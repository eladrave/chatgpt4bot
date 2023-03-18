CREATE DATABASE IF NOT EXISTS your_database_name;
USE your_database_name;

CREATE TABLE chat (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    DateTime DATETIME NOT NULL,
    `From` VARCHAR(20) NOT NULL,
    `To` VARCHAR(20) NOT NULL,
    Role ENUM('system', 'user', 'assistant') NOT NULL,
    Message TEXT NOT NULL
);
