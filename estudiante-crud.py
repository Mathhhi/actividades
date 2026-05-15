estudiantes = []

def mostrar_menu():
    print("\n--- MENU DE ESTUDIANTES ---")
    print("1. Agregar estudiante")
    print("2. Ver todos los estudiantes")
    print("3. Buscar estudiante por nombre")
    print("4. Buscar estudiante por ID")
    print("5. Actualizar estudiante")
    print("6. Eliminar estudiante")
    print("7. Ver estadisticas")
    print("8. Salir")

def agregar_estudiante():
    print("\n--- AGREGAR ESTUDIANTE ---")

    id_estudiante = input("ID del estudiante: ").strip()
    if id_estudiante == "":
        print("El ID no puede estar vacio.")
        return
    for e in estudiantes:
        if e["id"] == id_estudiante:
            print("Ya existe un estudiante con ese ID.")
            return

    nombre = input("Nombre: ").strip()
    if nombre == "":
        print("El nombre no puede estar vacio.")
        return

    try:
        edad = int(input("Edad: "))
    except ValueError:
        print("Edad invalida.")
        return

    try:
        nota = float(input("Nota (0 a 10): "))
        if nota < 0 or nota > 10:
            print("La nota debe estar entre 0 y 10.")
            return
    except ValueError:
        print("Nota invalida.")
        return

    if nota >= 6:
        estado = "Aprobado"
    else:
        estado = "Reprobado"

    estudiante = {"id": id_estudiante, "nombre": nombre, "edad": edad, "nota": nota, "estado": estado}
    estudiantes.append(estudiante)
    print(f"Estudiante agregado. Estado: {estado}")

def ver_estudiantes():
    print("\n--- LISTA DE ESTUDIANTES ---")
    if len(estudiantes) == 0:
        print("No hay estudiantes registrados.")
        return
    for e in estudiantes:
        print(f"ID: {e['id']} | Nombre: {e['nombre']} | Edad: {e['edad']} | Nota: {e['nota']} | Estado: {e['estado']}")

def buscar_por_nombre():
    print("\n--- BUSCAR POR NOMBRE ---")
    nombre = input("Ingrese el nombre a buscar: ").strip()
    encontrado = False
    for e in estudiantes:
        if e["nombre"].lower() == nombre.lower():
            print(f"ID: {e['id']} | Nombre: {e['nombre']} | Edad: {e['edad']} | Nota: {e['nota']} | Estado: {e['estado']}")
            encontrado = True
    if not encontrado:
        print("Estudiante no encontrado.")

def buscar_por_id():
    print("\n--- BUSCAR POR ID ---")
    id_estudiante = input("Ingrese el ID a buscar: ").strip()
    for e in estudiantes:
        if e["id"] == id_estudiante:
            print(f"ID: {e['id']} | Nombre: {e['nombre']} | Edad: {e['edad']} | Nota: {e['nota']} | Estado: {e['estado']}")
            return
    print("Estudiante no encontrado.")

def actualizar_estudiante():
    print("\n--- ACTUALIZAR ESTUDIANTE ---")
    id_estudiante = input("Ingrese el ID del estudiante a actualizar: ").strip()
    for e in estudiantes:
        if e["id"] == id_estudiante:
            print(f"Estudiante encontrado: {e['nombre']}")

            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre == "":
                print("El nombre no puede estar vacio.")
                return

            try:
                nueva_edad = int(input("Nueva edad: "))
            except ValueError:
                print("Edad invalida.")
                return

            try:
                nueva_nota = float(input("Nueva nota (0 a 10): "))
                if nueva_nota < 0 or nueva_nota > 10:
                    print("La nota debe estar entre 0 y 10.")
                    return
            except ValueError:
                print("Nota invalida.")
                return

            if nueva_nota >= 6:
                nuevo_estado = "Aprobado"
            else:
                nuevo_estado = "Reprobado"

            e["nombre"] = nuevo_nombre
            e["edad"] = nueva_edad
            e["nota"] = nueva_nota
            e["estado"] = nuevo_estado
            print(f"Estudiante actualizado. Nuevo estado: {nuevo_estado}")
            return

    print("Estudiante no encontrado.")

def eliminar_estudiante():
    print("\n--- ELIMINAR ESTUDIANTE ---")
    id_estudiante = input("Ingrese el ID del estudiante a eliminar: ").strip()
    for e in estudiantes:
        if e["id"] == id_estudiante:
            estudiantes.remove(e)
            print("Estudiante eliminado.")
            return
    print("Estudiante no encontrado.")

def ver_estadisticas():
    print("\n--- ESTADISTICAS ---")
    if len(estudiantes) == 0:
        print("No hay estudiantes registrados.")
        return

    total = len(estudiantes)
    aprobados = 0
    reprobados = 0
    suma_notas = 0

    for e in estudiantes:
        suma_notas += e["nota"]
        if e["estado"] == "Aprobado":
            aprobados += 1
        else:
            reprobados += 1

    promedio = suma_notas / total

    print(f"Total de estudiantes  : {total}")
    print(f"Aprobados             : {aprobados}")
    print(f"Reprobados            : {reprobados}")
    print(f"Promedio general      : {promedio:.2f}")

    print("\nDetalle por estudiante:")
    for e in estudiantes:
        print(f"  {e['nombre']} - Nota: {e['nota']} - {e['estado']}")


while True:
    mostrar_menu()
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        agregar_estudiante()
    elif opcion == "2":
        ver_estudiantes()
    elif opcion == "3":
        buscar_por_nombre()
    elif opcion == "4":
        buscar_por_id()
    elif opcion == "5":
        actualizar_estudiante()
    elif opcion == "6":
        eliminar_estudiante()
    elif opcion == "7":
        ver_estadisticas()
    elif opcion == "8":
        print("Hasta luego.")
        break
    else:
        print("Opcion no valida. Intente de nuevo.")