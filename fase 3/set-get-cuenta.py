class CuentaBancaria:
    def __init__(self):
        self.__saldo = 0

    def get_saldo(self):
        return self.__saldo
    
    def set_saldo(self, nuevo_saldo):
        if nuevo_saldo >= 0:
            self.__saldo = nuevo_saldo
        else:
            print("Error: El saldo no puede ser negativo")

cuenta1 = CuentaBancaria("juan", 300000)
print(cuenta1.get_saldo())

cuenta1.set_saldo(-90000)
print("Saldo actualizado:  ", cuenta1.get_saldo())