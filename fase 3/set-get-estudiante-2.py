class Estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.__nota = nota
    
    def get_nota(self):
        return self.__nota
    
    def set_nota(self, nueva_nota):
        if nueva_nota >= 0 and nueva_nota <= 5:
            self.__nota = nueva_nota
        else:
            print("Error: Nota invalida") 


estudiantes =[]

for i in range (3):
    print(f"registro estudiante {i + 1}")
    
    nombre =input("ingrese nombre: ")
    
    while True:
        nota =float(input("ingrese nota: "))
        
        if 0 <= nota <= 5:
            break;
        else:
            print("Error: Nota invalida")
    
    e = Estudiante(nombre, nota)
    estudiantes.append(e)        


print("\n--- Lista de Estudiantes ---")

for est in estudiantes:
    print("nombre: ", est.nombre)
    print("nota: ", est.get_nota(), "\n")
        