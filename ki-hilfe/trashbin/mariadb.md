CREATE DATABASE poiapp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'poiuser'@'localhost' IDENTIFIED BY 'geheim'; -- Passwort anpassen
GRANT ALL PRIVILEGES ON poiapp.* TO 'poiuser'@'localhost';

USE poiapp;

CREATE TABLE entries (
  id INT AUTO_INCREMENT PRIMARY KEY,
  poi VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL
);
