precios = [2000, 1500, 3000, 5000]

suma = 0
for p in precios:
    suma += p
    promedio = suma / len(precios)

print(f"El promedio de los precios es: {promedio}")