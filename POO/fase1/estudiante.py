class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera


estudiante1 = Estudiante("juan", 4, 5)
print("Nombre:", estudiante1.nombre)
print("Edad:", estudiante1.edad)
print("Carrera:", estudiante1.carrera)
