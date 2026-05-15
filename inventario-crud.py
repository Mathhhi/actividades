class Producto:
    def __init__(self, codigo, nombre, precio, cantidad, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria


productos = []


def mostrar_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Registrar producto")
    print("2. Mostrar todos los productos")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Calcular valor total del inventario")
    print("7. Mostrar productos agotados")
    print("8. Guardar inventario en archivo")
    print("9. Salir")


def registrar_producto():
    print("\n--- REGISTRAR PRODUCTO ---")

    codigo = input("Codigo: ").strip()
    if codigo == "":
        print("El codigo no puede estar vacio.")
        return

    for p in productos:
        if p.codigo == codigo:
            print("Ya existe un producto con ese codigo.")
            return

    nombre = input("Nombre: ").strip()
    if nombre == "":
        print("El nombre no puede estar vacio.")
        return

    try:
        precio = float(input("Precio: "))
    except ValueError:
        print("Precio invalido.")
        return

    if precio < 0:
        print("El precio no puede ser negativo.")
        return

    try:
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("Cantidad invalida.")
        return

    if cantidad < 0:
        print("La cantidad no puede ser negativa.")
        return

    categoria = input("Categoria: ").strip()
    if categoria == "":
        print("La categoria no puede estar vacia.")
        return

    nuevo = Producto(codigo, nombre, precio, cantidad, categoria)
    productos.append(nuevo)
    print("Producto registrado correctamente.")


def mostrar_productos():
    print("\n--- LISTA DE PRODUCTOS ---")
    if len(productos) == 0:
        print("No hay productos registrados.")
        return
    for p in productos:
        print("Codigo: " + p.codigo + " | Nombre: " + p.nombre + " | Precio: " + str(p.precio) + " | Cantidad: " + str(p.cantidad) + " | Categoria: " + p.categoria)


def buscar_producto():
    print("\n--- BUSCAR PRODUCTO ---")
    print("1. Por codigo")
    print("2. Por nombre")
    opcion = input("Seleccione: ").strip()

    if opcion == "1":
        codigo = input("Ingrese el codigo: ").strip()
        for p in productos:
            if p.codigo == codigo:
                print("Encontrado -> Codigo: " + p.codigo + " | Nombre: " + p.nombre + " | Precio: " + str(p.precio) + " | Cantidad: " + str(p.cantidad) + " | Categoria: " + p.categoria)
                return
        print("Producto no encontrado.")

    elif opcion == "2":
        nombre = input("Ingrese el nombre: ").strip()
        encontrado = False
        for p in productos:
            if p.nombre.lower() == nombre.lower():
                print("Codigo: " + p.codigo + " | Nombre: " + p.nombre + " | Precio: " + str(p.precio) + " | Cantidad: " + str(p.cantidad) + " | Categoria: " + p.categoria)
                encontrado = True
        if not encontrado:
            print("Producto no encontrado.")
    else:
        print("Opcion no valida.")


def actualizar_producto():
    print("\n--- ACTUALIZAR PRODUCTO ---")
    codigo = input("Ingrese el codigo del producto a actualizar: ").strip()

    for p in productos:
        if p.codigo == codigo:
            print("Producto encontrado: " + p.nombre)

            try:
                nuevo_precio = float(input("Nuevo precio: "))
            except ValueError:
                print("Precio invalido.")
                return

            if nuevo_precio < 0:
                print("El precio no puede ser negativo.")
                return

            try:
                nueva_cantidad = int(input("Nueva cantidad: "))
            except ValueError:
                print("Cantidad invalida.")
                return

            if nueva_cantidad < 0:
                print("La cantidad no puede ser negativa.")
                return

            nueva_categoria = input("Nueva categoria: ").strip()
            if nueva_categoria == "":
                print("La categoria no puede estar vacia.")
                return

            p.precio = nuevo_precio
            p.cantidad = nueva_cantidad
            p.categoria = nueva_categoria
            print("Producto actualizado correctamente.")
            return

    print("Producto no encontrado.")


def eliminar_producto():
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese el codigo del producto a eliminar: ").strip()

    for p in productos:
        if p.codigo == codigo:
            productos.remove(p)
            print("Producto eliminado correctamente.")
            return

    print("Producto no encontrado.")


def calcular_total_inventario():
    print("\n--- VALOR TOTAL DEL INVENTARIO ---")
    total = 0
    for p in productos:
        total = total + (p.precio * p.cantidad)
    print("El valor total del inventario es: " + str(total))


def mostrar_agotados():
    print("\n--- PRODUCTOS AGOTADOS ---")
    hay_agotados = False
    for p in productos:
        if p.cantidad == 0:
            print("Codigo: " + p.codigo + " | Nombre: " + p.nombre + " | Categoria: " + p.categoria)
            hay_agotados = True
    if not hay_agotados:
        print("No hay productos agotados.")


def guardar_archivo():
    archivo = open("inventario.txt", "w")
    archivo.write("=== INVENTARIO ===\n\n")
    if len(productos) == 0:
        archivo.write("No hay productos registrados.\n")
    else:
        for p in productos:
            linea = "Codigo: " + p.codigo + " | Nombre: " + p.nombre + " | Precio: " + str(p.precio) + " | Cantidad: " + str(p.cantidad) + " | Categoria: " + p.categoria + "\n"
            archivo.write(linea)
    archivo.close()
    print("Inventario guardado en inventario.txt")


while True:
    mostrar_menu()
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        registrar_producto()
    elif opcion == "2":
        mostrar_productos()
    elif opcion == "3":
        buscar_producto()
    elif opcion == "4":
        actualizar_producto()
    elif opcion == "5":
        eliminar_producto()
    elif opcion == "6":
        calcular_total_inventario()
    elif opcion == "7":
        mostrar_agotados()
    elif opcion == "8":
        guardar_archivo()
    elif opcion == "9":
        print("Hasta luego.")
        break
    else:
        print("Opcion no valida. Intente de nuevo.")