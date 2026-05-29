from src.estadistica import calcular_promedio
from src.estadistica import promedio_diccionario, contar_aprobados, clasificar_notas

datos = [10,15,20,25,30]

resultado = calcular_promedio(datos)

print("El promedio es:", resultado)

notas = {
    "juan":3.3,
    "maria":4.2,    
    "pedro":4.6,
    "ana":3.9,
}

promedio_notas = promedio_diccionario(notas)
print("El promedio de las notas es:", promedio_notas)

aprobados = contar_aprobados(notas, 3.5)
print("Cantidad de aprobados:", aprobados)

clasificacion = clasificar_notas(notas, 3.5)
print("Clasificación de notas:", clasificacion)

