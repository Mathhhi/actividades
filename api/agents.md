# API InMemoriam — Documentación del Proyecto

## Descripción

API REST desarrollada con **Spring Boot 4.2** y **Java 21** para la gestión completa (CRUD) de registros de difuntos. Conectada a **MySQL via JDBC** sin ORM (`JdbcTemplate`). Permite crear, consultar (con paginación), actualizar y eliminar registros de la tabla `difuntos`, además de contar con una interfaz web responsiva integrada.

---

## Estructura del Proyecto

```
api/
├── src/
│   └── main/
│       ├── java/com/microservicioInmemoriam/api/
│       │   ├── ApiApplication.java          ← Clase principal Spring Boot
│       │   ├── config/
│       │   │   └── CorsConfig.java          ← Configuración global de CORS (GET, POST, PUT, DELETE, OPTIONS)
│       │   ├── controller/
│       │   │   └── DifuntoController.java   ← REST Controller con CRUD completo
│       │   ├── model/
│       │   │   └── Difunto.java             ← Modelo / Entidad
│       │   ├── repository/
│       │   │   └── DifuntoRepository.java   ← Acceso a datos con JdbcTemplate (SQL directo)
│       │   └── service/
│       │       └── DifuntoService.java      ← Lógica de negocio y validaciones
│       └── resources/
│           ├── static/
│           │   ├── index.html               ← Interfaz gráfica web (HTML5)
│           │   ├── styles.css               ← Estilos modernos modo oscuro (CSS3)
│           │   └── app.js                   ← Lógica frontend cliente REST (JavaScript ES6+)
│           ├── application.properties       ← Configuración de la app y MySQL
│           └── db/
│               └── schema.sql              ← Script de creación de BD y tabla
├── logs/
│   └── api-inmemoriam.log                  ← Logs del sistema con rotación
└── pom.xml                                 ← Dependencias Maven
```

---

## Modelo: `Difunto`

| Campo             | Tipo        | Descripción                          | Obligatorio |
|-------------------|-------------|--------------------------------------|-------------|
| `id`              | `int`       | Identificador único autoincremental | Auto (PK)   |
| `nombre`          | `String`    | Nombre del difunto                   | Sí          |
| `apellido`        | `String`    | Apellido del difunto                 | Sí          |
| `fechaNacimiento` | `LocalDate` | Fecha de nacimiento (`yyyy-MM-dd`)   | No          |
| `fechaMuerte`     | `LocalDate` | Fecha de defunción (`yyyy-MM-dd`)    | Sí          |
| `lugarNacimiento` | `String`    | Ciudad / país de nacimiento          | No          |
| `lugarMuerte`     | `String`    | Ciudad / país de fallecimiento       | No          |
| `causaMuerte`     | `String`    | Causa del deceso                     | No          |
| `epitafio`        | `String`    | Mensaje recordatorio                 | No          |
| `activo`          | `boolean`   | Estado del registro (1 / 0)          | Sí          |

---

## Base de Datos MySQL

- **Host:** `localhost:3306`
- **Base de datos:** `db_inmemoriam`
- **Usuario:** `root`
- **Contraseña:** `Root`

### Esquema SQL (`src/main/resources/db/schema.sql`)

```sql
CREATE DATABASE IF NOT EXISTS db_inmemoriam CHARACTER SET utf8mb4;

USE db_inmemoriam;

CREATE TABLE IF NOT EXISTS difuntos (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    nombre              VARCHAR(100)  NOT NULL,
    apellido            VARCHAR(100)  NOT NULL,
    fecha_nacimiento    DATE          NULL,
    fecha_muerte        DATE          NOT NULL,
    lugar_nacimiento    VARCHAR(200)  NULL,
    lugar_muerte        VARCHAR(200)  NULL,
    causa_muerte        VARCHAR(300)  NULL,
    epitafio            TEXT          NULL,
    activo              TINYINT(1)    NOT NULL DEFAULT 1,
    fecha_registro      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP     NULL     ON UPDATE CURRENT_TIMESTAMP
);
```

---

## Endpoints REST (CRUD Completo)

Base URL: `http://localhost:8081/api/difuntos`

### 1. `GET /api/difuntos` — Consulta paginada

| Parámetro | Tipo  | Default | Descripción                      |
|-----------|-------|---------|----------------------------------|
| `page`    | `int` | `0`     | Número de página (inicia en 0)   |
| `size`    | `int` | `10`    | Registros por página (1 a 100)   |

**Respuesta exitosa `200 OK`:**
```json
{
  "datos": [
    {
      "id": 1,
      "nombre": "Gabriel",
      "apellido": "García Márquez",
      "fechaNacimiento": "1927-03-06",
      "fechaMuerte": "2014-04-17",
      "lugarNacimiento": "Aracataca, Colombia",
      "lugarMuerte": "Ciudad de México, México",
      "causaMuerte": "Infección respiratoria",
      "epitafio": "Vivirá en sus palabras para siempre.",
      "activo": true
    }
  ],
  "paginaActual": 0,
  "tamañoPagina": 10,
  "totalRegistros": 5,
  "totalPaginas": 1,
  "esPrimera": true,
  "esUltima": true
}
```

---

### 2. `GET /api/difuntos/{id}` — Consulta por ID

**Respuesta exitosa `200 OK`:**
```json
{
  "datos": {
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fechaNacimiento": "1927-03-06",
    "fechaMuerte": "2014-04-17",
    "lugarNacimiento": "Aracataca, Colombia",
    "lugarMuerte": "Ciudad de México, México",
    "causaMuerte": "Infección respiratoria",
    "epitafio": "Vivirá en sus palabras para siempre.",
    "activo": true
  },
  "mensaje": "Difunto encontrado correctamente"
}
```

---

### 3. `POST /api/difuntos` — Crear registro

**Cuerpo de la petición (JSON):**
```json
{
  "nombre": "Jorge Luis",
  "apellido": "Borges",
  "fechaNacimiento": "1899-08-24",
  "fechaMuerte": "1986-06-14",
  "lugarNacimiento": "Buenos Aires, Argentina",
  "lugarMuerte": "Ginebra, Suiza",
  "causaMuerte": "Cáncer hepático",
  "epitafio": "Que no haya una sola cosa que no sea una palabra.",
  "activo": true
}
```

**Respuesta exitosa `201 CREATED`:**
```json
{
  "mensaje": "Difunto registrado correctamente.",
  "datos": {
    "id": 6,
    "nombre": "Jorge Luis",
    "apellido": "Borges",
    "fechaNacimiento": "1899-08-24",
    "fechaMuerte": "1986-06-14",
    "lugarNacimiento": "Buenos Aires, Argentina",
    "lugarMuerte": "Ginebra, Suiza",
    "causaMuerte": "Cáncer hepático",
    "epitafio": "Que no haya una sola cosa que no sea una palabra.",
    "activo": true
  }
}
```

---

### 4. `PUT /api/difuntos/{id}` — Actualizar registro existente

**Cuerpo de la petición (JSON):**
```json
{
  "nombre": "Gabriel",
  "apellido": "García Márquez",
  "fechaNacimiento": "1927-03-06",
  "fechaMuerte": "2014-04-17",
  "lugarNacimiento": "Aracataca, Colombia",
  "lugarMuerte": "Ciudad de México, México",
  "causaMuerte": "Infección respiratoria",
  "epitafio": "La vida no es la que uno vivió, sino la que uno recuerda.",
  "activo": true
}
```

**Respuesta exitosa `200 OK`:**
```json
{
  "mensaje": "Difunto actualizado correctamente.",
  "datos": {
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    ...
  }
}
```

---

### 5. `DELETE /api/difuntos/{id}` — Eliminar registro

**Respuesta exitosa `200 OK`:**
```json
{
  "mensaje": "Difunto con id 1 eliminado correctamente.",
  "id": 1,
  "eliminado": true
}
```

---

## Manejo de Errores y Códigos HTTP

| Código | Significado | Motivo |
|--------|-------------|--------|
| `200`  | OK | Consulta, actualización o eliminación exitosa |
| `201`  | Created | Creación de registro exitosa |
| `400`  | Bad Request | Parámetros inválidos, campos obligatorios faltantes o registro inexistente |
| `500`  | Internal Server Error | Excepción no controlada o error en la base de datos |

**Formato estándar de error:**
```json
{
  "error": true,
  "codigo": 400,
  "mensaje": "El campo 'nombre' es obligatorio."
}
```

---

## Interfaz Web Gráfica

Ubicada en `src/main/resources/static/`:
- **`index.html`**: Estructura de componentes (toolbar, tabla paginada, detalle, modal crear/editar, modal confirmación).
- **`styles.css`**: Diseño moderno en modo oscuro, adaptable a dispositivos móviles.
- **`app.js`**: Cliente JavaScript asíncrono (`fetch`) para todas las operaciones CRUD y actualización reactiva de la interfaz.

---

## Cómo Ejecutar el Proyecto

```powershell
# 1. Configurar JAVA_HOME con JDK 21 (si no está persistido)
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.13.10002-hotspot"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

# 2. Entrar al directorio del proyecto
cd c:\Users\APRENDIZ\Downloads\api\api

# 3. Compilar y ejecutar
.\mvnw.cmd spring-boot:run -DskipTests
```

Acceder desde el navegador a: **[http://localhost:8081](http://localhost:8081)**
