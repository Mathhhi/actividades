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


student = []

for i in range(3):
    print(f"\nRegistro del estudiante {i+1}:")
    nombre = input(" nombre del estudiante: ")
    nota = float(input(" nota del estudiante: "))

    e = Estudiante(nombre, nota)
    student.append(e)

print("\nInformación de los estudiantes registrados:")
for e in student:
    print(e.mostrar_informacion())