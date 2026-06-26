CREATE DATABASE techstore DEFAULT CHARACTER SET = 'utf8mb4';

USE techstore;

CREATE TABLE productos(
codigo VARCHAR(20) PRIMARY KEY,
nombre VARCHAR(80) NOT NULL,
precio DECIMAL(10,2) NOT NULL,
categoria VARCHAR(50)
);

-- TRUNCATE productos;
INSERT INTO productos VALUES
('P001','Laptop Lenovo',3500000,'Computadores'),
('P002','Mouse Logitech',85000,'Accesorios'),
('P003','Monitor Samsung',890000,'Monitores'),
('P004', 'Portátil Lenovo IdeaPad 3', 2850000, 'Computadores');

SELECT * FROM productos;




