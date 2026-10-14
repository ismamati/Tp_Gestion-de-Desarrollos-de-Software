def buscar_por_materia(alumnos, materia):
    return [alumno for alumno in alumnos if alumno["materia"] == materia]


def esta_aprobado(alumno):
    return alumno["nota"] >= 6


def reporte_curso(alumnos):
    cantidad = len(alumnos)
    suma_notas = 0
    nombres = []
    materias = []
    mejor_alumno = ""
    mejor_nota = 0
    for alumno in alumnos:
        suma_notas += alumno["nota"]
        nombres.append(alumno["nombre"])
        if alumno["materia"] not in materias:
            materias.append(alumno["materia"])
        if alumno["nota"] > mejor_nota:
            mejor_nota = alumno["nota"]
            mejor_alumno = alumno["nombre"]
    promedio = 0
    if cantidad > 0:
        promedio = round(suma_notas / cantidad, 1)
    return {
        "cantidad": cantidad,
        "promedio": promedio,
        "nombres": sorted(nombres),
        "materias": materias,
        "mejor_alumno": mejor_alumno,
        "mejor_nota": mejor_nota,
    }


def reporte_aprobados(alumnos):
    aprobados = [alumno for alumno in alumnos if esta_aprobado(alumno)]
    #return reporte_curso(aprobados)
