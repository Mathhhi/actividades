def calcular_promedio(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)


def promedio_diccionario(diccionario):
    if not diccionario:
        return 0
    return sum(diccionario.values()) / len(diccionario)


def contar_aprobados(diccionario, nota_minima):
    return sum(1 for nota in diccionario.values() if nota >= nota_minima)


def clasificar_notas(diccionario, nota_minima):
    clasificacion = {}
    for estudiante, nota in diccionario.items():
        if nota >= nota_minima:
            clasificacion[estudiante] = "Aprobado"
        else:
            clasificacion[estudiante] = "Reprobado"
    return clasificacion
