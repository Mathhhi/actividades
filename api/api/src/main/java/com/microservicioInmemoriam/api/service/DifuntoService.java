package com.microservicioInmemoriam.api.service;

import com.microservicioInmemoriam.api.model.Difunto;
import com.microservicioInmemoriam.api.repository.DifuntoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DifuntoService {

    private static final Logger logger = LoggerFactory.getLogger(DifuntoService.class);

    private final DifuntoRepository difuntoRepository;

    public DifuntoService(DifuntoRepository difuntoRepository) {
        this.difuntoRepository = difuntoRepository;
    }

    /**
     * Retorna listado paginado de difuntos con metadatos de paginación
     */
    public Map<String, Object> consultarDifuntos(int page, int size) {
        logger.info("Iniciando consulta paginada de difuntos - página: {}, tamaño: {}", page, size);

        List<Difunto> difuntos = difuntoRepository.findAll(page, size);
        int totalRegistros = difuntoRepository.countAll();
        int totalPaginas = (int) Math.ceil((double) totalRegistros / size);

        Map<String, Object> respuesta = new HashMap<>();
        respuesta.put("datos", difuntos);
        respuesta.put("paginaActual", page);
        respuesta.put("tamañoPagina", size);
        respuesta.put("totalRegistros", totalRegistros);
        respuesta.put("totalPaginas", totalPaginas);
        respuesta.put("esPrimera", page == 0);
        respuesta.put("esUltima", page >= totalPaginas - 1);

        logger.info("Consulta completada - {} difuntos encontrados, {} páginas en total", difuntos.size(), totalPaginas);
        return respuesta;
    }

    /**
     * Retorna un difunto por su ID
     */
    public Difunto consultarPorId(int id) {
        logger.info("Consultando difunto con id: {}", id);
        Difunto difunto = difuntoRepository.findById(id);
        if (difunto == null) {
            logger.warn("No se encontró difunto con id: {}", id);
        } else {
            logger.info("Difunto encontrado: {} {}", difunto.getNombre(), difunto.getApellido());
        }
        return difunto;
    }

    /**
     * Crea un nuevo registro de difunto
     */
    public Difunto crearDifunto(Difunto difunto) {
        logger.info("Registrando nuevo difunto: {} {}", difunto.getNombre(), difunto.getApellido());
        Difunto nuevo = difuntoRepository.create(difunto);
        logger.info("Difunto registrado exitosamente con id: {}", nuevo.getId());
        return nuevo;
    }

    /**
     * Actualiza un difunto existente por su ID
     */
    public Difunto actualizarDifunto(int id, Difunto difunto) {
        logger.info("Iniciando actualización del difunto con id: {}", id);
        Difunto existente = difuntoRepository.findById(id);
        if (existente == null) {
            logger.warn("Intento de actualizar difunto inexistente con id: {}", id);
            return null;
        }

        difunto.setId(id);
        int filasAfectadas = difuntoRepository.update(id, difunto);
        if (filasAfectadas > 0) {
            logger.info("Difunto con id: {} actualizado correctamente", id);
            return difunto;
        } else {
            logger.error("No se pudo actualizar el difunto con id: {}", id);
            return null;
        }
    }

    /**
     * Elimina un difunto por su ID
     */
    public boolean eliminarDifunto(int id) {
        logger.info("Iniciando eliminación del difunto con id: {}", id);
        Difunto existente = difuntoRepository.findById(id);
        if (existente == null) {
            logger.warn("Intento de eliminar difunto inexistente con id: {}", id);
            return false;
        }
        int filasAfectadas = difuntoRepository.deleteById(id);
        boolean eliminado = filasAfectadas > 0;
        if (eliminado) {
            logger.info("Difunto con id: {} eliminado correctamente", id);
        } else {
            logger.error("No se pudo eliminar el difunto con id: {}", id);
        }
        return eliminado;
    }
}
