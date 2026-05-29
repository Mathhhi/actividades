productos = {
    "manzana": 2000,
    "banana": 1500,
    "naranja": 3000,
    "pera": 5000
}

mayor = 0
producto_mas_caro = ""

for producto, precio in productos.items():
    if precio > mayor:
        mayor = precio
        producto_mas_caro = producto
print(f"El producto más caro es: {producto_mas_caro} con un precio de {mayor}")