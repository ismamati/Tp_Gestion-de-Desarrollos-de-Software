from app.notas import buscar_por_materia, esta_aprobado, reporte_curso

ALUMNOS = [
    {"nombre": "Ana", "materia": "Historia", "nota": 8},
    {"nombre": "Bruno", "materia": "Geografia", "nota": 4},
    {"nombre": "Carla", "materia": "Historia", "nota": 9},
]


def test_buscar_por_materia():
    resultado = buscar_por_materia(ALUMNOS, "Historia")
    assert [alumno["nombre"] for alumno in resultado] == ["Ana", "Carla"]


def test_buscar_por_materia_sin_resultados():
    assert buscar_por_materia(ALUMNOS, "Musica") == []


def test_esta_aprobado():
    assert esta_aprobado(ALUMNOS[0])
    assert not esta_aprobado(ALUMNOS[1])


def test_reporte_curso():
    assert reporte_curso(ALUMNOS) == {
        "cantidad": 3,
        "promedio": 7.0,
        "nombres": ["Ana", "Bruno", "Carla"],
        "materias": ["Historia", "Geografia"],
        "mejor_alumno": "Carla",
        "mejor_nota": 9,
    }


def test_reporte_curso_vacio():
    reporte = reporte_curso([])
    assert reporte["cantidad"] == 0
    assert reporte["promedio"] == 0
