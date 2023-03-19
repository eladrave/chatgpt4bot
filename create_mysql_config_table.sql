-- Create the `config` table
CREATE TABLE IF NOT EXISTS config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `From` VARCHAR(20) NOT NULL,
    `To` VARCHAR(20) NOT NULL,
    ConfigKey VARCHAR(255) NOT NULL,
    ConfigValue TEXT NOT NULL
);
