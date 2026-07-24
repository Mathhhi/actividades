CREATE DATABASE IF NOT EXISTS techstore DEFAULT CHARACTER SET = 'utf8mb4';

USE techstore;

CREATE TABLE IF NOT EXISTS productos(
codigo VARCHAR(20) PRIMARY KEY,
nombre VARCHAR(80) NOT NULL,
precio DECIMAL(10,2) NOT NULL,
categoria VARCHAR(50)
);

-- TRUNCATE productos;
INSERT IGNORE INTO productos VALUES
('P001','Laptop Lenovo',3500000,'Computadores'),
('P002','Mouse Logitech',85000,'Accesorios'),
('P003','Monitor Samsung',890000,'Monitores'),
('P004', 'Portátil Lenovo IdeaPad 3', 2850000, 'Computadores');

SELECT * FROM productos;

CREATE TABLE IF NOT EXISTS usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'usuario') DEFAULT 'usuario',
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo'
);

INSERT INTO usuarios (nombre, correo, contraseña, rol, estado)
VALUES ('John Doe', 'john.doe@example.com', 'scrypt:32768:8:1$v1M2Ytw1ystB1swH$c0d65b0f69f2ca68a0719e93ecd82cdb5ba970714e90f4bdb0fc04b4ce21ff063a679d6cc470ce30b74e50606d33b5c8b44e0ea640e979dd291bcad5e24f1f1e', 'Administrador', 'Activo')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), contraseña=VALUES(contraseña), rol=VALUES(rol), estado=VALUES(estado);


