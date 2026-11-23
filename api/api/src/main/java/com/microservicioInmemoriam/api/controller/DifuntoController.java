package com.microservicioInmemoriam.api.controller;

import com.microservicioInmemoriam.api.model.Difunto;
import com.microservicioInmemoriam.api.service.DifuntoService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/difuntos")
@CrossOrigin(origins = "*", allowedHeaders = "*", methods = {
        RequestMethod.GET,
        RequestMethod.POST,
        RequestMethod.PUT,
        RequestMethod.DELETE,
        RequestMethod.OPTIONS
})
public class DifuntoController {

    private static final Logger logger = LoggerFactory.getLogger(DifuntoController.class);

    private final DifuntoService difuntoService;

    public DifuntoController(DifuntoService difuntoService) {
        this.difuntoService = difuntoService;
    }

    /**
     * GET /api/difuntos?page=0&size=10
     * Consulta paginada de todos los difuntos
     */
    @GetMapping
    public ResponseEntity<Map<String, Object>> consultarDifuntos(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        logger.info("Solicitud GET /api/difuntos - page={}, size={}", page, size);

        try {
            if (page < 0) {
                logger.warn("Parámetro 'page' inválido: {}", page);
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El parámetro 'page' no puede ser negativo.");
            }
            if (size <= 0 || size > 100) {
                logger.warn("Parámetro 'size' inválido: {}", size);
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El parámetro 'size' debe estar entre 1 y 100.");
            }

            Map<String, Object> resultado = difuntoService.consultarDifuntos(page, size);
            logger.info("Respuesta exitosa GET /api/difuntos");
            return ResponseEntity.ok(resultado);

        } catch (Exception e) {
            logger.error("Error interno al consultar difuntos: {}", e.getMessage(), e);
            return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
                    "Error interno del servidor al consultar difuntos.");
        }
    }

    /**
     * GET /api/difuntos/{id}
     * Consulta de un difunto por ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<Map<String, Object>> consultarPorId(@PathVariable int id) {

        logger.info("Solicitud GET /api/difuntos/{}", id);

        try {
            if (id <= 0) {
                logger.warn("ID inválido recibido: {}", id);
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El ID debe ser un número entero positivo.");
            }

            Difunto difunto = difuntoService.consultarPorId(id);

            if (difunto == null) {
                logger.warn("Difunto con id {} no encontrado", id);
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "No se encontró el difunto con id: " + id);
            }

            Map<String, Object> respuesta = new HashMap<>();
            respuesta.put("datos", difunto);
            respuesta.put("mensaje", "Difunto encontrado correctamente");

            logger.info("Respuesta exitosa GET /api/difuntos/{}", id);
            return ResponseEntity.ok(respuesta);

        } catch (Exception e) {
            logger.error("Error interno al consultar difunto con id {}: {}", id, e.getMessage(), e);
            return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
                    "Error interno del servidor al consultar el difunto.");
        }
    }

    /**
     * POST /api/difuntos
     * Registrar un nuevo difunto
     */
    @PostMapping
    public ResponseEntity<Map<String, Object>> crearDifunto(@RequestBody Difunto difunto) {
        logger.info("Solicitud POST /api/difuntos - nuevo registro para: {} {}",
                difunto.getNombre(), difunto.getApellido());

        try {
            if (difunto.getNombre() == null || difunto.getNombre().trim().isEmpty()) {
                logger.warn("Validación fallida: 'nombre' es nulo o vacío");
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El campo 'nombre' es obligatorio.");
            }
            if (difunto.getApellido() == null || difunto.getApellido().trim().isEmpty()) {
                logger.warn("Validación fallida: 'apellido' es nulo o vacío");
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El campo 'apellido' es obligatorio.");
            }
            if (difunto.getFechaMuerte() == null) {
                logger.warn("Validación fallida: 'fechaMuerte' es obligatoria");
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El campo 'fechaMuerte' es obligatorio.");
            }

            Difunto creado = difuntoService.crearDifunto(difunto);

            Map<String, Object> respuesta = new HashMap<>();
            respuesta.put("mensaje", "Difunto registrado correctamente.");
            respuesta.put("datos", creado);

            logger.info("Difunto creado exitosamente con id: {}", creado.getId());
            return ResponseEntity.status(HttpStatus.CREATED).body(respuesta);

        } catch (Exception e) {
            logger.error("Error interno al crear difunto: {}", e.getMessage(), e);
            return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
                    "Error interno del servidor al registrar el difunto.");
        }
    }

    /**
     * PUT /api/difuntos/{id}
     * Actualizar los datos de un difunto existente
     */
    @PutMapping("/{id}")
    public ResponseEntity<Map<String, Object>> actualizarDifunto(
            @PathVariable int id,
            @RequestBody Difunto difunto) {

        logger.info("Solicitud PUT /api/difuntos/{}", id);

        try {
            if (id <= 0) {
                logger.warn("ID inválido para actualización: {}", id);
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El ID debe ser un número entero positivo.");
            }
            if (difunto.getNombre() == null || difunto.getNombre().trim().isEmpty()) {
                logger.warn("Validación fallida: 'nombre' es nulo o vacío");
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El campo 'nombre' es obligatorio.");
            }
            if (difunto.getApellido() == null || difunto.getApellido().trim().isEmpty()) {
                logger.warn("Validación fallida: 'apellido' es nulo o vacío");
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El campo 'apellido' es obligatorio.");
            }
            if (difunto.getFechaMuerte() == null) {
                logger.warn("Validación fallida: 'fechaMuerte' es obligatoria");
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El campo 'fechaMuerte' es obligatorio.");
            }

            Difunto actualizado = difuntoService.actualizarDifunto(id, difunto);

            if (actualizado == null) {
                logger.warn("No se pudo actualizar: difunto con id {} no existe", id);
                return buildErrorResponse(HttpStatus.BAD_REQUEST,
                        "No se encontró el difunto con id: " + id + ". No se pudo actualizar.");
            }

            Map<String, Object> respuesta = new HashMap<>();
            respuesta.put("mensaje", "Difunto actualizado correctamente.");
            respuesta.put("datos", actualizado);

            logger.info("Difunto con id {} actualizado correctamente", id);
            return ResponseEntity.ok(respuesta);

        } catch (Exception e) {
            logger.error("Error interno al actualizar difunto con id {}: {}", id, e.getMessage(), e);
            return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
                    "Error interno del servidor al actualizar el difunto.");
        }
    }

    /**
     * DELETE /api/difuntos/{id}
     * Eliminar un difunto por ID
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, Object>> eliminarDifunto(@PathVariable int id) {

        logger.info("Solicitud DELETE /api/difuntos/{}", id);

        try {
            if (id <= 0) {
                logger.warn("ID inválido para eliminación: {}", id);
                return buildErrorResponse(HttpStatus.BAD_REQUEST, "El ID debe ser un número entero positivo.");
            }

            boolean eliminado = difuntoService.eliminarDifunto(id);

            if (!eliminado) {
                logger.warn("No se pudo eliminar - difunto con id {} no existe", id);
                return buildErrorResponse(HttpStatus.BAD_REQUEST,
                        "No se encontró el difunto con id: " + id + ". No se realizó ninguna eliminación.");
            }

            Map<String, Object> respuesta = new HashMap<>();
            respuesta.put("mensaje", "Difunto con id " + id + " eliminado correctamente.");
            respuesta.put("id", id);
            respuesta.put("eliminado", true);

            logger.info("Difunto con id {} eliminado - respuesta exitosa", id);
            return ResponseEntity.ok(respuesta);

        } catch (Exception e) {
            logger.error("Error interno al eliminar difunto con id {}: {}", id, e.getMessage(), e);
            return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
                    "Error interno del servidor al eliminar el difunto.");
        }
    }

    // ─── Método auxiliar ────────────────────────────────────────────────────────

    private ResponseEntity<Map<String, Object>> buildErrorResponse(HttpStatus status, String mensaje) {
        Map<String, Object> error = new HashMap<>();
        error.put("error", true);
        error.put("codigo", status.value());
        error.put("mensaje", mensaje);
        return ResponseEntity.status(status).body(error);
    }
}
