productos = {
    "manzana": 2000,
    "banana": 1500,
    "naranja": 3000,
    "pera": 5000
}

for nombre, precio in productos.items():
    if precio > 3000:
        print(nombre,"es caro COP",precio)