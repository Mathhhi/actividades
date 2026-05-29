precios = [2000, 1500, 3000, 5000]

precios_con_iva = []

for p in precios:
    iva = p * 0.19
    precio_con_iva = p + iva
    precios_con_iva.append(precio_con_iva)

print(f"Los precios con IVA son: {precios_con_iva}")