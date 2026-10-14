# Guía para entender y presentar DevSecOps

Preparación para el jueves 15 de octubre de 2026. Esta guía propone pasos para que el equipo los realice; no modifica las funciones ni los PR existentes.

## 1. Qué hace nuestra aplicación

Es un módulo de Python para trabajar con notas de alumnos. No hay interfaz web, servidor ni base de datos. Los datos son una lista de diccionarios; los tests usan tres alumnos:

| Alumno | Materia | Nota |
| --- | --- | --- |
| Ana | Historia | 8 |
| Bruno | Geografia | 4 |
| Carla | Historia | 9 |

El archivo `app/notas.py` tiene tres funciones:

- `buscar_por_materia(alumnos, materia)`: devuelve los alumnos de esa materia. Para Historia, devuelve Ana y Carla.
- `esta_aprobado(alumno)`: devuelve `True` si la nota es al menos 6. Ana aprueba; Bruno no.
- `reporte_curso(alumnos)`: calcula cantidad, promedio, nombres ordenados, materias y mejor alumno. Con estos datos devuelve 3 alumnos, promedio 7,0 y Carla como mejor alumna, con 9.

La aplicación no guarda ni cambia las notas: consulta datos que recibe. `tests/test_notas.py` contiene cinco tests que comprueban esas funciones, incluyendo una búsqueda sin resultados y un curso vacío.

`requirements.txt` enumera paquetes que se instalan: pytest ejecuta los tests; pytest-cov mide cobertura; python-multipart es una dependencia vulnerable incorporada al ejemplo, pero el código de notas no la usa.

## 2. La idea que queremos demostrar

**Que los tests pasen no alcanza para decidir si un cambio está listo para integrarse.** También revisamos su mantenibilidad, la seguridad del código y sus dependencias.

Pensalo como tres preguntas:

1. ¿Hace lo que esperamos? → Tests.
2. ¿El cambio tiene problemas de calidad o seguridad? → SonarCloud.
3. ¿Usamos librerías con vulnerabilidades conocidas? → Dependabot.

GitHub Actions automatiza los controles. Branch Protection exige que ciertos checks pasen antes de permitir el merge.

## 3. Conceptos, con ejemplos sencillos

| Concepto | Explicación | Ejemplo en este trabajo |
| --- | --- | --- |
| Deuda técnica | Trabajo futuro que genera una solución difícil de mantener. Puede ser una decisión consciente o una acumulación accidental. | Copiar el cálculo del reporte obliga a corregir dos funciones si cambia la fórmula. |
| Code Smell | Señal de un problema de mantenibilidad; no implica que el programa falle. | Una variable que se declara y nunca se usa. |
| Bug | Defecto que puede producir resultados incorrectos o errores. | Dividir por la cantidad de alumnos sin contemplar un curso vacío. Es un ejemplo conceptual, no un defecto observado en la función actual. |
| Vulnerabilidad | Debilidad de seguridad que podría explotarse. | Procesar entradas de una forma insegura o instalar una versión afectada por un aviso de seguridad. |
| Testing dinámico | Ejecutar código y comprobar resultados. | pytest verifica las funciones; Playwright, usado en otra actividad, comprueba comportamientos en un navegador. |
| SAST | Analizar el código sin ejecutar la aplicación. | SonarCloud busca patrones de errores y problemas de seguridad o mantenibilidad. |
| Cobertura | Porcentaje del código que se ejecutó durante los tests. | Si agregamos una función y ningún test la llama, esas líneas quedan sin cubrir. |
| Duplicación | Bloques de código repetidos que aumentan el costo de cambios. | El PR de demostración copia el cuerpo de `reporte_curso`. |
| Quality Gate | Reglas que deciden si las métricas de un análisis son aceptables. | Fallar si hay Bugs/Vulnerabilidades nuevos o cobertura nueva menor al 80%. |
| CI / pipeline | Secuencia automática de pasos que verifica un cambio. | Instalar Python → dependencias → tests y cobertura → SonarCloud. |
| Pull Request (PR) | Propuesta para integrar cambios de una rama en otra. | Proponer `reporte_aprobados` desde `demo-code-smell` hacia `main`. |
| Branch Protection | Requisitos que GitHub aplica antes de permitir integrar cambios. | Exigir `tests` y `SonarCloud Code Analysis` en verde. |
| DevSecOps | Integrar seguridad y calidad al trabajo habitual de desarrollo y automatización. | Analizar cada PR y mantener vigiladas las dependencias. |

El 100% de cobertura no significa que hayamos probado todas las situaciones posibles: indica ejecución, no la calidad de las comprobaciones. Un test puede ejecutar una línea sin verificar correctamente su resultado.

## 4. Seguridad de las dependencias

Las librerías ajenas también forman parte de nuestra aplicación. Podemos escribir código correcto y usar una versión con una vulnerabilidad conocida. Además, un atacante podría comprometer una cuenta que publica paquetes o distribuir un paquete malicioso: esos son ejemplos de ataques a la cadena de suministro.

Una vulnerabilidad conocida no significa necesariamente que hubo un ataque. Dependabot detecta versiones afectadas consultando el grafo de dependencias y avisos de seguridad, y puede proponer un PR de actualización. No detecta por sí solo cualquier paquete malicioso.

En nuestro repositorio, `python-multipart==0.0.6` está afectado por [CVE-2024-24762](https://github.com/advisories/GHSA-2jv5-9r88-3w3p), una denegación de servicio al procesar ciertos encabezados en aplicaciones que usan formularios. No necesitamos ejecutar ningún ataque para mostrar la alerta.

**SonarCloud y Dependabot cubren controles distintos.** En esta actividad, el gate de SonarCloud controla nuestro código; Dependabot vigila las dependencias. Una alerta de Dependabot no se convierte automáticamente en un fallo del gate de SonarCloud.

## 5. Qué tenemos hecho

Estado consultado el 13/10/2026; revisar de nuevo antes de grabar:

| Elemento | Estado |
| --- | --- |
| Módulo Python y cinco tests | Ya existe. |
| Workflow de GitHub Actions | Ya existe en `.github/workflows/ci.yml`. |
| Reportes de cobertura | El CI genera `coverage.xml` para SonarCloud y un reporte HTML descargable. |
| Vinculación con SonarCloud | Ya funciona; no hay que empezar de cero. |
| Análisis después de los tests | Ya está agregado al workflow. |
| Espera del Quality Gate | Activa para PR; en pushes a `main` se envía el análisis sin esperar su resultado. |
| Gate con umbral de 80% | Comprobado en el PR #2. También controla Bugs, Vulnerabilidades y duplicación. |
| PR con problema intencional | [PR #2: Agrego reporte de aprobados](https://github.com/ismamati/Tp_Gestion-de-Desarrollos-de-Software/pull/2), abierto. |
| Fallo real de calidad | En ese PR: 4,8% de cobertura nueva y 82,8% de duplicación. Los tests pasan; falla el análisis de SonarCloud. |
| Dependabot proponiendo actualización | [PR #1](https://github.com/ismamati/Tp_Gestion-de-Desarrollos-de-Software/pull/1), abierto, propone actualizar python-multipart a 0.0.31. |

## 6. Qué falta

1. **Verificar el bloqueo del merge.** Consultar Branch Protection con la cuenta administradora. No se pudo comprobar su configuración con la API pública: pide autenticación.
2. **Grabar el estado rojo.** Mostrar el diff del PR #2, tests que pasan, gate que falla y mensaje de merge bloqueado.
3. **Corregir el PR #2 y agregar tests de la función nueva.** No basta con borrar la variable sin usar: el fallo observado es por duplicación y cobertura.
4. **Hacer push y comprobar el estado verde.** Mostrar el nuevo análisis y el merge habilitado cuando se cumplan todas las condiciones.
5. **Mostrar Dependabot y el aviso.** Revisar la configuración de alertas y actualizaciones de seguridad; después de registrar la evidencia, integrar la corrección si corresponde.
6. **Completar las diapositivas con capturas reales** y ensayar quién explica cada parte.

## 7. Camino recomendado: usar el PR existente

Es la ruta con menos cambios antes del jueves: el fallo ya está comprobado. No conviene rehacer toda la demo si esta funciona.

### Paso 1. Recorrer los archivos

Abrir `app/notas.py`, `tests/test_notas.py`, `requirements.txt`, `sonar-project.properties` y `.github/workflows/ci.yml`. Entender la finalidad de cada uno. En el workflow, señalar el orden y el argumento `sonar.qualitygate.wait`.

### Paso 2. Revisar el gate

Abrir el [proyecto de SonarCloud](https://sonarcloud.io/dashboard?id=ismamati_Tp_Gestion-de-Desarrollos-de-Software) → **Quality Gate**. Mostrar Bugs/Vulnerabilidades nuevos en cero y cobertura del código nuevo mínima de 80%. Con el plan gratuito pueden usar el gate incorporado Sonar way; no hace falta contratar un plan para esta demo.

En esa página, desmarcar **Ignore duplication and coverage on small changes** y guardar si quieren que la cobertura se exija incluso en una corrección muy corta. Por defecto, estos controles pueden ignorarse con menos de 20 líneas nuevas. Ver la [configuración oficial](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/changing-quality-gate).

### Paso 3. Revisar la protección de `main`

En GitHub → **Settings → Branches**, revisar la regla de `main`:

- Exigir un PR antes de integrar.
- Activar **Require status checks to pass before merging**.
- Elegir los nombres reales de los checks: `tests` y `SonarCloud Code Analysis`.
- Si presentan con la cuenta administradora, aplicar también las restricciones a administradores; revisar **Do not allow bypassing the above settings**. Si usan rulesets, revisar su lista de bypass.

Mostrar el mensaje real de bloqueo en el PR. Un check rojo no impide el merge si no es obligatorio. Ver [ramas protegidas en GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

### Paso 4. Registrar la evidencia roja

Abrir el PR #2 → **Files changed**. Mostrar que `reporte_aprobados` repite el cálculo existente y declara `total_inscriptos` sin usar. Luego abrir **Checks** y el análisis de SonarCloud del PR. Explicar: “Los tests existentes no llaman a la función nueva. Pasan, pero la función quedó casi sin cobertura y repite código”.

Mostrar **4,8% de cobertura nueva**, **82,8% de duplicación** y el gate en rojo. No atribuir el fallo a la variable sin usar: la condición de mantenibilidad de ese análisis pasa.

### Paso 5. Trabajar sobre la rama del PR

En PowerShell, desde la carpeta del repositorio y con los cambios propios guardados:

```powershell
git status
git fetch origin
git switch demo-code-smell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

La rama ya existe en GitHub. Si Git no crea automáticamente la rama local, usar `git switch --track origin/demo-code-smell`. Añadir `.venv/` a `.gitignore` para no subir el entorno virtual.

### Paso 6. Reemplazar la función duplicada

En `app/notas.py`, conservar las otras funciones y reemplazar **todo el cuerpo y la definición anterior de `reporte_aprobados`** por:

```python
def reporte_aprobados(alumnos):
    aprobados = [alumno for alumno in alumnos if esta_aprobado(alumno)]
    return reporte_curso(aprobados)
```

La segunda línea selecciona los aprobados. La tercera usa el reporte que ya existe. Para Ana, Bruno y Carla, devuelve un reporte de Ana y Carla con promedio 8,5. Se evita mantener dos copias del mismo cálculo.

### Paso 7. Agregar tests que verifiquen la nueva función

Agregar `reporte_aprobados` al import de `tests/test_notas.py` y añadir:

```python
def test_reporte_aprobados():
    reporte = reporte_aprobados(ALUMNOS)
    assert reporte["cantidad"] == 2
    assert reporte["nombres"] == ["Ana", "Carla"]
    assert reporte["promedio"] == 8.5


def test_reporte_aprobados_sin_aprobados():
    assert reporte_aprobados([ALUMNOS[1]]) == reporte_curso([])


def test_reporte_aprobados_nota_limite():
    alumno = {"nombre": "Diego", "materia": "Historia", "nota": 6}
    assert reporte_aprobados([alumno])["cantidad"] == 1
```

Se comprueban el filtro y el promedio, el caso sin aprobados y la nota límite. No agregamos tests solamente para colorear la cobertura: verifican resultados útiles.

### Paso 8. Ejecutar, revisar y hacer push

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=app --cov-report=xml --cov-report=html
git diff
git add app/notas.py tests/test_notas.py .gitignore
git commit -m "Reutilizo el reporte y pruebo el filtro de aprobados"
git push origin demo-code-smell
```

El push actualiza el PR #2; no abrir otro PR para la corrección. Esperar a que finalice Actions y el análisis de SonarCloud. Revisar los motivos si queda rojo: puede haber otro requisito, un error de análisis o una condición de revisión pendiente.

### Paso 9. Grabar la evidencia verde

Mostrar el nuevo commit, los checks verdes, el gate aprobado y el merge habilitado. Si Branch Protection exige revisiones o resolver conversaciones, también hay que cumplirlas. No usar la opción de saltar requisitos para demostrar éxito.

### Paso 10. Mostrar Dependabot

En GitHub → **Settings → Advanced Security**, comprobar Dependency graph, Dependabot alerts y Dependabot security updates. En **Security → Dependabot**, abrir la alerta. Mostrar el PR #1 y su cambio de versión.

No hace falta `dependabot.yml` para las actualizaciones de seguridad; sirve para configurar, entre otras cosas, actualizaciones periódicas de versiones. Ver la [guía oficial de actualizaciones de seguridad](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates).

## 8. Ejemplo alternativo más corto: contar aprobados

Este ejemplo es opcional para aprender o hacer una nueva demo. No es el código del PR #2 ni tiene un resultado de SonarCloud verificado. Para la entrega recomiendo el PR existente.

En una nueva rama desde `main`, agregar a `app/notas.py`:

```python
def contar_aprobados(alumnos):
    etiqueta = "Aprobados"
    aprobados = [alumno for alumno in alumnos if esta_aprobado(alumno)]
    return len(aprobados)
```

La función devuelve 2 con nuestros datos. `etiqueta` no se usa: es el Code Smell que queremos mostrar. **No agregar todavía tests de esta función** al primer commit.

Al abrir un PR, los tests antiguos deberían seguir pasando, pero estas líneas nuevas quedan sin ejecutar. Con el control de cobertura para cambios pequeños activo, esperamos que el gate falle por cobertura nueva menor al 80%. La detección de la variable depende de las reglas activas y un Code Smell aislado no garantiza un gate rojo.

Para corregir, borrar `etiqueta` y agregar `contar_aprobados` al import de los tests. Añadir:

```python
def test_contar_aprobados():
    assert contar_aprobados(ALUMNOS) == 2


def test_contar_aprobados_lista_vacia():
    assert contar_aprobados([]) == 0


def test_contar_aprobados_nota_limite():
    alumno = {"nombre": "Diego", "materia": "Historia", "nota": 6}
    assert contar_aprobados([alumno]) == 1
```

Hacer push a la misma rama del nuevo PR y comprobar el resultado. Esta alternativa permite explicar en pocas líneas: función útil, variable innecesaria, tests ausentes, gate rojo, corrección y tests nuevos.

## 9. Organización hasta el jueves

- **Martes 13:** todos leen las secciones 1–6; una persona verifica gate y protección, otra prepara las diapositivas y otra repasa Dependabot. Registrar la evidencia roja antes de cambiar la rama.
- **Miércoles 14:** corregir el PR, comprobar verde y completar las capturas. Ensayar una vez el recorrido completo y repartir la explicación según la cantidad de integrantes.
- **Jueves 15:** revisar acceso a las cuentas y enlaces; usar las capturas como respaldo y mostrar los resultados reales. Evitar rehacer configuraciones durante la exposición.

La presentación editable `PRESENTACION_DEVSECOPS.pptx` tiene una estructura preparada y notas para hablar. Completar nombres y capturas; el estado verde todavía debe producirse y comprobarse.

## 10. Preguntas que pueden hacerles

**¿Por qué pasan los tests y falla el pipeline?** Porque los tests existentes comprueban las funciones antiguas. El pipeline incluye otro control que detecta problemas en el cambio nuevo.

**¿Por qué cobertura nueva y no solamente cobertura total?** Un proyecto grande puede mantener un porcentaje global alto aunque una función nueva esté sin probar. El gate del PR revisa el cambio.

**¿SonarCloud ejecuta los tests?** En este proyecto los ejecuta pytest en Actions. SonarCloud importa el reporte de cobertura y analiza el código.

**¿Un Code Smell es una vulnerabilidad?** No. Un Code Smell es una señal de mantenibilidad; una vulnerabilidad es una debilidad de seguridad.

**¿Dependabot bloquea automáticamente el merge?** No por el mero hecho de generar una alerta o un PR. El bloqueo de esta demo se obtiene haciendo obligatorios los checks de CI y SonarCloud.

**¿Ya terminamos la consigna?** Tenemos la integración y el fallo de demostración. Falta verificar el bloqueo, registrar la corrección en verde y preparar la exposición.
