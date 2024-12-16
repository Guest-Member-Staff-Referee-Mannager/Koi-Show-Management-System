-- Tạo cơ sở dữ liệu koi_exhibition
CREATE DATABASE IF NOT EXISTS koi_exhibition;

-- Sử dụng cơ sở dữ liệu koi_exhibition
USE koi_exhibition;

-- Tạo bảng koi_fish để lưu thông tin các cá Koi
CREATE TABLE IF NOT EXISTS koi_fish (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image VARCHAR(255) NOT NULL,
    serial_number VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    description TEXT
);

-- Thêm dữ liệu mẫu
INSERT INTO koi_fish (image, serial_number, name, breed, age, description)
VALUES 
('koi1.jpg', 'K01', 'Kohaku', 'Kohaku', 2, 'Cá có hoa văn đỏ trắng đẹp mắt.'),
('koi2.jpg', 'K02', 'Showa', 'Showa', 3, 'Màu sắc đen trắng đỏ tương phản rõ nét.'),
('koi3.jpg', 'K03', 'Sanke', 'Taisho Sanke', 1, 'Hoa văn đỏ đen trên nền trắng nổi bật.');
