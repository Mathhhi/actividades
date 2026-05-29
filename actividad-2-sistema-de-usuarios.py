class Usuario:
    def __init__(self, documento, nombre, correo, rol, estado):
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.rol = rol
        self.estado = estado


usuarios = []

roles_validos = ["administrador", "aprendiz", "instructor"]


def mostrar_menu():
    print("\n--- MENU DE USUARIOS ---")
    print("1. Registrar usuario")
    print("2. Mostrar todos los usuarios")
    print("3. Buscar usuario")
    print("4. Actualizar usuario")
    print("5. Eliminar usuario")
    print("6. Mostrar usuarios activos")
    print("7. Contar usuarios por rol")
    print("8. Exportar usuarios a archivo")
    print("9. Salir")


def correo_valido(correo):
    if "@" in correo and "." in correo:
        return True
    return False


def registrar_usuario():
    print("\n--- REGISTRAR USUARIO ---")

    documento = input("Documento: ").strip()
    if documento == "":
        print("El documento no puede estar vacio.")
        return
    for u in usuarios:
        if u.documento == documento:
            print("Ya existe un usuario con ese documento.")
            return

    nombre = input("Nombre: ").strip()
    if nombre == "":
        print("El nombre no puede estar vacio.")
        return

    correo = input("Correo electronico: ").strip()
    if correo == "":
        print("El correo no puede estar vacio.")
        return
    if not correo_valido(correo):
        print("El correo no es valido. Debe contener @ y un punto.")
        return

    print("Roles disponibles: administrador, aprendiz, instructor")
    rol = input("Rol: ").strip().lower()
    if rol == "":
        print("El rol no puede estar vacio.")
        return
    if rol not in roles_validos:
        print("El rol no es valido. Debe ser: administrador, aprendiz o instructor.")
        return

    print("Estado: activo o inactivo")
    estado = input("Estado: ").strip().lower()
    if estado != "activo" and estado != "inactivo":
        print("El estado debe ser activo o inactivo.")
        return

    nuevo = Usuario(documento, nombre, correo, rol, estado)
    usuarios.append(nuevo)
    print("Usuario registrado correctamente.")


def mostrar_usuarios():
    print("\n--- LISTA DE USUARIOS ---")
    if len(usuarios) == 0:
        print("No hay usuarios registrados.")
        return
    for u in usuarios:
        print("Documento: " + u.documento + " | Nombre: " + u.nombre + " | Correo: " + u.correo + " | Rol: " + u.rol + " | Estado: " + u.estado)


def buscar_usuario():
    print("\n--- BUSCAR USUARIO ---")
    print("1. Por documento")
    print("2. Por correo")
    opcion = input("Seleccione: ").strip()

    if opcion == "1":
        documento = input("Ingrese el documento: ").strip()
        for u in usuarios:
            if u.documento == documento:
                print("Encontrado -> Documento: " + u.documento + " | Nombre: " + u.nombre + " | Correo: " + u.correo + " | Rol: " + u.rol + " | Estado: " + u.estado)
                return
        print("Usuario no encontrado.")

    elif opcion == "2":
        correo = input("Ingrese el correo: ").strip()
        for u in usuarios:
            if u.correo.lower() == correo.lower():
                print("Encontrado -> Documento: " + u.documento + " | Nombre: " + u.nombre + " | Correo: " + u.correo + " | Rol: " + u.rol + " | Estado: " + u.estado)
                return
        print("Usuario no encontrado.")

    else:
        print("Opcion no valida.")


def actualizar_usuario():
    print("\n--- ACTUALIZAR USUARIO ---")
    documento = input("Ingrese el documento del usuario a actualizar: ").strip()

    for u in usuarios:
        if u.documento == documento:
            print("Usuario encontrado: " + u.nombre)

            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre == "":
                print("El nombre no puede estar vacio.")
                return

            nuevo_correo = input("Nuevo correo: ").strip()
            if nuevo_correo == "":
                print("El correo no puede estar vacio.")
                return
            if not correo_valido(nuevo_correo):
                print("El correo no es valido.")
                return

            print("Roles disponibles: administrador, aprendiz, instructor")
            nuevo_rol = input("Nuevo rol: ").strip().lower()
            if nuevo_rol not in roles_validos:
                print("El rol no es valido.")
                return

            nuevo_estado = input("Nuevo estado (activo/inactivo): ").strip().lower()
            if nuevo_estado != "activo" and nuevo_estado != "inactivo":
                print("El estado debe ser activo o inactivo.")
                return

            u.nombre = nuevo_nombre
            u.correo = nuevo_correo
            u.rol = nuevo_rol
            u.estado = nuevo_estado
            print("Usuario actualizado correctamente.")
            return

    print("Usuario no encontrado.")


def eliminar_usuario():
    print("\n--- ELIMINAR USUARIO ---")
    documento = input("Ingrese el documento del usuario a eliminar: ").strip()

    for u in usuarios:
        if u.documento == documento:
            usuarios.remove(u)
            print("Usuario eliminado correctamente.")
            return

    print("Usuario no encontrado.")


def mostrar_activos():
    print("\n--- USUARIOS ACTIVOS ---")
    hay_activos = False
    for u in usuarios:
        if u.estado == "activo":
            print("Documento: " + u.documento + " | Nombre: " + u.nombre + " | Correo: " + u.correo + " | Rol: " + u.rol)
            hay_activos = True
    if not hay_activos:
        print("No hay usuarios activos.")


def contar_roles():
    print("\n--- CONTEO POR ROL ---")
    if len(usuarios) == 0:
        print("No hay usuarios registrados.")
        return

    administradores = 0
    aprendices = 0
    instructores = 0

    for u in usuarios:
        if u.rol == "administrador":
            administradores = administradores + 1
        elif u.rol == "aprendiz":
            aprendices = aprendices + 1
        elif u.rol == "instructor":
            instructores = instructores + 1

    print("Administradores : " + str(administradores))
    print("Aprendices      : " + str(aprendices))
    print("Instructores    : " + str(instructores))


def guardar_archivo():
    archivo = open("usuarios.txt", "w")
    archivo.write("=== LISTA DE USUARIOS ===\n\n")
    if len(usuarios) == 0:
        archivo.write("No hay usuarios registrados.\n")
    else:
        for u in usuarios:
            linea = "Documento: " + u.documento + " | Nombre: " + u.nombre + " | Correo: " + u.correo + " | Rol: " + u.rol + " | Estado: " + u.estado + "\n"
            archivo.write(linea)
    archivo.close()
    print("Usuarios exportados correctamente a usuarios.txt")


while True:
    mostrar_menu()
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        mostrar_usuarios()
    elif opcion == "3":
        buscar_usuario()
    elif opcion == "4":
        actualizar_usuario()
    elif opcion == "5":
        eliminar_usuario()
    elif opcion == "6":
        mostrar_activos()
    elif opcion == "7":
        contar_roles()
    elif opcion == "8":
        guardar_archivo()
    elif opcion == "9":
        print("Hasta luego.")
        break
    else:
        print("Opcion no valida. Intente de nuevo.")