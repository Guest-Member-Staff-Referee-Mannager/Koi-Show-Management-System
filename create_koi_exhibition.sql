CREATE DATABASE IF NOT EXISTS koi_exhibition;

USE koi_exhibition;

CREATE TABLE IF NOT EXISTS koi_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    koi_id INT NOT NULL, 
    image VARCHAR(255) NOT NULL,
    serial_number VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    description TEXT,
    FOREIGN KEY (koi_id) REFERENCES koi_fish(id) ON DELETE CASCADE 
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    password VARCHAR(255) 
);

SELECT * FROM users;

SELECT * FROM koi_fish;
