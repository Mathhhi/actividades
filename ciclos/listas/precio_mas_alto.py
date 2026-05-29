precios = [2000, 1500, 3000, 5000]

mayor = precios[0]

for p in precios:
    if p > mayor:
        mayor = p

print(f"El precio más alto es: {mayor}")