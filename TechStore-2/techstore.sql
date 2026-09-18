CREATE DATABASE IF NOT EXISTS techstore DEFAULT CHARACTER SET = 'utf8mb4';

USE techstore;

CREATE TABLE IF NOT EXISTS usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'cliente') NOT NULL DEFAULT 'cliente',
    estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS productos(
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    imagen VARCHAR(255) NOT NULL
);

ALTER TABLE productos ADD COLUMN IF NOT EXISTS imagen VARCHAR(255) NOT NULL DEFAULT 'default-product.svg';
ALTER TABLE productos MODIFY nombre VARCHAR(100) NOT NULL;

ALTER TABLE usuarios CHANGE COLUMN password contrasena VARCHAR(255) NOT NULL;
ALTER TABLE usuarios MODIFY nombre VARCHAR(100) NOT NULL;
ALTER TABLE usuarios MODIFY correo VARCHAR(120) NOT NULL;
ALTER TABLE usuarios MODIFY telefono VARCHAR(20) NULL;
UPDATE usuarios SET rol = LOWER(rol), estado = LOWER(estado);
ALTER TABLE usuarios MODIFY rol ENUM('administrador', 'cliente') NOT NULL DEFAULT 'cliente';
ALTER TABLE usuarios MODIFY estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo';

INSERT INTO usuarios (nombre, correo, contrasena, rol, estado) VALUES
('Administrador Principal', 'admin@techstore.com', 'pbkdf2:sha256:1000000$96I4hv4rxqsyahHg$c73c571888267052231751d18b61ad273d2a37444ddeae4c9d1924a850351585', 'administrador', 'activo'),
('Administrador Secundario', 'admin2@techstore.com', 'pbkdf2:sha256:1000000$cVVOdVb2gFvXBhn4$f6dc67a5eb276f2821c5ecfa12d1269d3525c95e977d6d21e83bdb1673e08a1b', 'administrador', 'activo')
ON DUPLICATE KEY UPDATE correo = VALUES(correo);

INSERT INTO productos (codigo, nombre, precio, categoria, imagen) VALUES
('P001', 'Laptop Lenovo', 3500000, 'Computadores', 'default-product.svg'),
('P002', 'Mouse Logitech', 85000, 'Accesorios', 'default-product.svg'),
('P003', 'Monitor Samsung', 890000, 'Monitores', 'default-product.svg'),
('P004', 'Portatil Lenovo IdeaPad 3', 2850000, 'Computadores', 'default-product.svg')
ON DUPLICATE KEY UPDATE codigo = VALUES(codigo);

SELECT * FROM productos;