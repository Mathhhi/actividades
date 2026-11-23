package com.microservicioInmemoriam.api.model;

import java.time.LocalDate;

public class Difunto {

    private Integer id;
    private String nombre;
    private String apellido;
    private LocalDate fechaNacimiento;
    private LocalDate fechaMuerte;
    private String lugarNacimiento;
    private String lugarMuerte;
    private String causaMuerte;
    private String epitafio;
    private boolean activo = true;

    public Difunto() {
    }

    public Difunto(Integer id, String nombre, String apellido, LocalDate fechaNacimiento,
                   LocalDate fechaMuerte, String lugarNacimiento, String lugarMuerte,
                   String causaMuerte, String epitafio, boolean activo) {
        this.id = id;
        this.nombre = nombre;
        this.apellido = apellido;
        this.fechaNacimiento = fechaNacimiento;
        this.fechaMuerte = fechaMuerte;
        this.lugarNacimiento = lugarNacimiento;
        this.lugarMuerte = lugarMuerte;
        this.causaMuerte = causaMuerte;
        this.epitafio = epitafio;
        this.activo = activo;
    }

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getApellido() { return apellido; }
    public void setApellido(String apellido) { this.apellido = apellido; }

    public LocalDate getFechaNacimiento() { return fechaNacimiento; }
    public void setFechaNacimiento(LocalDate fechaNacimiento) { this.fechaNacimiento = fechaNacimiento; }

    public LocalDate getFechaMuerte() { return fechaMuerte; }
    public void setFechaMuerte(LocalDate fechaMuerte) { this.fechaMuerte = fechaMuerte; }

    public String getLugarNacimiento() { return lugarNacimiento; }
    public void setLugarNacimiento(String lugarNacimiento) { this.lugarNacimiento = lugarNacimiento; }

    public String getLugarMuerte() { return lugarMuerte; }
    public void setLugarMuerte(String lugarMuerte) { this.lugarMuerte = lugarMuerte; }

    public String getCausaMuerte() { return causaMuerte; }
    public void setCausaMuerte(String causaMuerte) { this.causaMuerte = causaMuerte; }

    public String getEpitafio() { return epitafio; }
    public void setEpitafio(String epitafio) { this.epitafio = epitafio; }

    public boolean isActivo() { return activo; }
    public void setActivo(boolean activo) { this.activo = activo; }
}
