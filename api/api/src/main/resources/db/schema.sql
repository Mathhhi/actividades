-- ============================================================
-- Script de creación de base de datos: db_inmemoriam
-- Microservicio: api-inmemoriam
-- ============================================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS db_inmemoriam
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE db_inmemoriam;

-- ============================================================
-- Tabla: difuntos
-- ============================================================
CREATE TABLE IF NOT EXISTS difuntos (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(100)  NOT NULL COMMENT 'Nombre del difunto',
    apellido         VARCHAR(100)  NOT NULL COMMENT 'Apellido del difunto',
    fecha_nacimiento DATE          NULL     COMMENT 'Fecha de nacimiento',
    fecha_muerte     DATE          NOT NULL COMMENT 'Fecha de fallecimiento',
    lugar_nacimiento VARCHAR(200)  NULL     COMMENT 'Ciudad/país de nacimiento',
    lugar_muerte     VARCHAR(200)  NULL     COMMENT 'Ciudad/país donde falleció',
    causa_muerte     VARCHAR(300)  NULL     COMMENT 'Causa del fallecimiento',
    epitafio         TEXT          NULL     COMMENT 'Epitafio o mensaje recordatorio',
    activo           TINYINT(1)    NOT NULL DEFAULT 1 COMMENT 'Registro activo (1) o eliminado lógicamente (0)',
    fecha_registro   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro en el sistema',
    fecha_actualizacion TIMESTAMP  NULL     ON UPDATE CURRENT_TIMESTAMP COMMENT 'Última actualización',

    INDEX idx_nombre    (nombre),
    INDEX idx_apellido  (apellido),
    INDEX idx_fecha_muerte (fecha_muerte),
    INDEX idx_activo    (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Registro de difuntos del sistema InMemoriam';

-- ============================================================
-- Datos de prueba
-- ============================================================
INSERT INTO difuntos (nombre, apellido, fecha_nacimiento, fecha_muerte, lugar_nacimiento, lugar_muerte, causa_muerte, epitafio, activo)
VALUES
('Gabriel', 'García Márquez',  '1927-03-06', '2014-04-17', 'Aracataca, Colombia',    'Ciudad de México, México', 'Infección respiratoria',       'Vivirá en sus palabras para siempre.',   1),
('Simón',   'Bolívar',         '1783-07-24', '1830-12-17', 'Caracas, Venezuela',     'Santa Marta, Colombia',   'Tuberculosis',                 'El Libertador de América.',               1),
('María',   'Concepción Lara', '1950-03-15', '2023-08-10', 'Medellín, Colombia',     'Bogotá, Colombia',        'Paro cardíaco',                'Siempre en nuestros corazones.',          1),
('Carlos',  'Rodríguez Peña',  '1945-11-02', '2024-01-22', 'Cali, Colombia',         'Cali, Colombia',          'Insuficiencia renal',          'Padre, abuelo y eterno compañero.',       1),
('Lucía',   'Fernández',       '1962-06-30', '2025-05-03', 'Barranquilla, Colombia', 'Barranquilla, Colombia',  'Cáncer de mama',               'Su amor iluminó cada rincón del hogar.', 1);
