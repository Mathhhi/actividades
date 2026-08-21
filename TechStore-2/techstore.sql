CREATE DATABASE IF NOT EXISTS techstore DEFAULT CHARACTER SET = 'utf8mb4';

USE techstore;

CREATE TABLE IF NOT EXISTS productos(
codigo VARCHAR(20) PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
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
    telefono VARCHAR(20) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Cliente', 'usuario') DEFAULT 'Cliente',
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo'
);

ALTER TABLE usuarios MODIFY rol ENUM('Administrador', 'Cliente', 'usuario') DEFAULT 'Cliente';
SET @telefono_existe = (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'telefono');
SET @sql_telefono = IF(@telefono_existe = 0, 'ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20) NOT NULL DEFAULT ''''', 'SELECT 1');
PREPARE stmt_telefono FROM @sql_telefono;
EXECUTE stmt_telefono;
DEALLOCATE PREPARE stmt_telefono;
UPDATE usuarios SET rol = 'Cliente' WHERE rol = 'usuario';

INSERT INTO usuarios (nombre, correo, telefono, contraseña, rol, estado)
VALUES ('John Doe', 'john.doe@example.com', '3000000002', 'scrypt:32768:8:1$v1M2Ytw1ystB1swH$c0d65b0f69f2ca68a0719e93ecd82cdb5ba970714e90f4bdb0fc04b4ce21ff063a679d6cc470ce30b74e50606d33b5c8b44e0ea640e979dd291bcad5e24f1f1e', 'Administrador', 'Activo')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), telefono=VALUES(telefono), contraseña=VALUES(contraseña), rol=VALUES(rol), estado=VALUES(estado);

INSERT INTO usuarios (nombre, correo, telefono, contraseña, rol, estado)
VALUES
('Administrador Principal', 'admin@techstore.com', '3000000000', 'scrypt:32768:8:1$Qa1v56zzJUhso5HE$ea99a1ab29ee0d7c76d7a678692403025b4a44021a5cbaf5cd07426f20766b0889aa8fb4d84afaad1e8dc6530bbc12d4fd3777045564a4eb3c134ce83cd77c06', 'Administrador', 'Activo'),
('Administrador Soporte', 'soporte@techstore.com', '3000000001', 'scrypt:32768:8:1$Qa1v56zzJUhso5HE$ea99a1ab29ee0d7c76d7a678692403025b4a44021a5cbaf5cd07426f20766b0889aa8fb4d84afaad1e8dc6530bbc12d4fd3777045564a4eb3c134ce83cd77c06', 'Administrador', 'Activo')
ON DUPLICATE KEY UPDATE telefono=VALUES(telefono), rol=VALUES(rol), estado=VALUES(estado);


