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

e1 = Estudiante("karen", 4.5)
print(e1.get_nota())

e1.set_nota(-2)   