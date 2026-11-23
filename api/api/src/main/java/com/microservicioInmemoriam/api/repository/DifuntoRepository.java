package com.microservicioInmemoriam.api.repository;

import com.microservicioInmemoriam.api.model.Difunto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

@Repository
public class DifuntoRepository {

    private static final Logger logger = LoggerFactory.getLogger(DifuntoRepository.class);

    private final JdbcTemplate jdbcTemplate;

    public DifuntoRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    private final RowMapper<Difunto> difuntoRowMapper = new RowMapper<Difunto>() {
        @Override
        public Difunto mapRow(ResultSet rs, int rowNum) throws SQLException {
            Difunto d = new Difunto();
            d.setId(rs.getInt("id"));
            d.setNombre(rs.getString("nombre"));
            d.setApellido(rs.getString("apellido"));
            d.setFechaNacimiento(rs.getDate("fecha_nacimiento") != null
                    ? rs.getDate("fecha_nacimiento").toLocalDate() : null);
            d.setFechaMuerte(rs.getDate("fecha_muerte") != null
                    ? rs.getDate("fecha_muerte").toLocalDate() : null);
            d.setLugarNacimiento(rs.getString("lugar_nacimiento"));
            d.setLugarMuerte(rs.getString("lugar_muerte"));
            d.setCausaMuerte(rs.getString("causa_muerte"));
            d.setEpitafio(rs.getString("epitafio"));
            d.setActivo(rs.getBoolean("activo"));
            return d;
        }
    };

    /**
     * Consulta paginada de difuntos
     */
    public List<Difunto> findAll(int page, int size) {
        int offset = page * size;
        String sql = "SELECT * FROM difuntos ORDER BY id LIMIT ? OFFSET ?";
        logger.debug("Consultando difuntos - página: {}, tamaño: {}, offset: {}", page, size, offset);
        return jdbcTemplate.query(sql, difuntoRowMapper, size, offset);
    }

    /**
     * Cuenta el total de registros para la paginación
     */
    public int countAll() {
        String sql = "SELECT COUNT(*) FROM difuntos";
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class);
        return count != null ? count : 0;
    }

    /**
     * Busca un difunto por ID
     */
    public Difunto findById(int id) {
        String sql = "SELECT * FROM difuntos WHERE id = ?";
        logger.debug("Buscando difunto con id: {}", id);
        List<Difunto> resultados = jdbcTemplate.query(sql, difuntoRowMapper, id);
        return resultados.isEmpty() ? null : resultados.get(0);
    }

    /**
     * Crea un nuevo registro de difunto y retorna el difunto con su ID generado
     */
    public Difunto create(Difunto difunto) {
        String sql = "INSERT INTO difuntos (nombre, apellido, fecha_nacimiento, fecha_muerte, lugar_nacimiento, lugar_muerte, causa_muerte, epitafio, activo) " +
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        logger.debug("Insertando nuevo difunto: {} {}", difunto.getNombre(), difunto.getApellido());

        KeyHolder keyHolder = new GeneratedKeyHolder();

        jdbcTemplate.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            ps.setString(1, difunto.getNombre());
            ps.setString(2, difunto.getApellido());
            ps.setDate(3, difunto.getFechaNacimiento() != null ? Date.valueOf(difunto.getFechaNacimiento()) : null);
            ps.setDate(4, difunto.getFechaMuerte() != null ? Date.valueOf(difunto.getFechaMuerte()) : null);
            ps.setString(5, difunto.getLugarNacimiento());
            ps.setString(6, difunto.getLugarMuerte());
            ps.setString(7, difunto.getCausaMuerte());
            ps.setString(8, difunto.getEpitafio());
            ps.setBoolean(9, difunto.isActivo());
            return ps;
        }, keyHolder);

        if (keyHolder.getKey() != null) {
            difunto.setId(keyHolder.getKey().intValue());
        }
        return difunto;
    }

    /**
     * Actualiza un difunto existente por ID
     */
    public int update(int id, Difunto difunto) {
        String sql = "UPDATE difuntos SET nombre = ?, apellido = ?, fecha_nacimiento = ?, fecha_muerte = ?, " +
                     "lugar_nacimiento = ?, lugar_muerte = ?, causa_muerte = ?, epitafio = ?, activo = ? " +
                     "WHERE id = ?";
        logger.debug("Actualizando difunto con id: {}", id);

        return jdbcTemplate.update(sql,
                difunto.getNombre(),
                difunto.getApellido(),
                difunto.getFechaNacimiento() != null ? Date.valueOf(difunto.getFechaNacimiento()) : null,
                difunto.getFechaMuerte() != null ? Date.valueOf(difunto.getFechaMuerte()) : null,
                difunto.getLugarNacimiento(),
                difunto.getLugarMuerte(),
                difunto.getCausaMuerte(),
                difunto.getEpitafio(),
                difunto.isActivo(),
                id
        );
    }

    /**
     * Elimina un difunto por ID
     */
    public int deleteById(int id) {
        String sql = "DELETE FROM difuntos WHERE id = ?";
        logger.debug("Eliminando difunto con id: {}", id);
        return jdbcTemplate.update(sql, id);
    }
}
