productos = {
    "manzana": 2000,
    "banana": 1500,
    "naranja": 3000,
    "pera": 5000
}

total = 0
for precio in productos.values():
    total += precio
print(f"El inventario total es: {total}")