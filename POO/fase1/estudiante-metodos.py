class Estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota

    def mostrar_informacion(self):
        if self.nota >= 3:
            estado = "Aprobado"
        else:
            estado = "Reprobado"

        return f"Nombre: {self.nombre}, Nota: {self.nota}, Estado: {estado}"


# Ejemplo de uso
estudiante1 = Estudiante("Juan", 4.5)
estudiante2 = Estudiante("María", 2.8)

print(estudiante1.mostrar_informacion())
print(estudiante2.mostrar_informacion())