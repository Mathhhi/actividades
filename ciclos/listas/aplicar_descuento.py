precios = [2000, 1500, 3000, 5000]

for p in precios:
    descuento = p * 0.10
    precio_con_descuento = p - descuento
    print(f"El precio original es: {p}, el descuento es: {descuento}, el precio con descuento es: {precio_con_descuento}")