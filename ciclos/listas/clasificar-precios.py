precios = [2000, 1500, 3000, 5000]

for p in precios:
    if p > 2000:
        print("barato: ", p)
    elif p <= 4000:
        print("medio: ", p)