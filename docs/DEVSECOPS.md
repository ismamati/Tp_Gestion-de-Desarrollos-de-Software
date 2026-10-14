# Calidad de código, deuda técnica y seguridad

Guía de la actividad y del video, adaptada a este repositorio. Estado consultado el 13 de octubre de 2026 (Argentina). Los resultados pueden cambiar con nuevos pushes.

## Qué está funcionando y qué falta verificar

| Requisito | Evidencia observada |
| --- | --- |
| Repositorio público vinculado con SonarCloud | El [dashboard](https://sonarcloud.io/dashboard?id=ismamati_Tp_Gestion-de-Desarrollos-de-Software) devuelve métricas del proyecto. |
| Tests antes del análisis | `.github/workflows/ci.yml` ejecuta pytest, genera cobertura y luego invoca SonarScanner mediante la acción oficial. |
| Fallo del pipeline por Quality Gate | En el [workflow del PR #2](https://github.com/ismamati/Tp_Gestion-de-Desarrollos-de-Software/actions/runs/38488425815), los tests pasan y el step de SonarCloud falla. La API de SonarCloud confirma que el gate del PR está en `ERROR`. |
| Bugs y vulnerabilidades nuevos | El resultado del gate del PR incluye condiciones que fallan si `new_bugs > 0` o `new_vulnerabilities > 0`. |
| Cobertura mínima del 80% | El gate del PR falla con cobertura del código nuevo de 4,8%, por debajo del 80%. |
| Dependabot | Está abierto el [PR #1](https://github.com/ismamati/Tp_Gestion-de-Desarrollos-de-Software/pull/1), creado por Dependabot para actualizar `python-multipart` de 0.0.6 a 0.0.31. |
| Bloqueo de merge | Pendiente de verificar con una sesión administradora. La consulta pública de Branch Protection devuelve HTTP 401; los checks rojos por sí solos no prueban que el merge esté bloqueado. |
| Corrección y checks verdes | Pendiente: corregir el PR #2, hacer push y mostrar el resultado real. |

La consulta de `main` muestra cobertura global de 100%, 0 Bugs, 0 Vulnerabilidades, 0 Code Smells y 0% de duplicación. La cobertura global de `main` no reemplaza la cobertura del código nuevo de un PR.

## Conceptos para explicar

**Deuda técnica.** Son costos futuros de mantenimiento derivados de decisiones de diseño o implementación. Por ejemplo, copiar una función permite terminar rápido, pero después obliga a modificar dos lugares ante cada cambio. La deuda puede ser deliberada si se registra y se programa su corrección; también puede acumularse por falta de revisión.

**Code Smells.** Son señales de problemas de mantenibilidad, como variables sin usar, funciones demasiado complejas o responsabilidades mezcladas. El programa puede funcionar y tener estos problemas. A largo plazo aumentan el tiempo para comprender, cambiar y probar el código. La duplicación también genera deuda, aunque SonarCloud la mide separadamente de los Code Smells.

**Testing dinámico y SAST.** Playwright ejecuta la aplicación y comprueba comportamientos del usuario. Los tests de pytest de este proyecto también ejecutan código: verifican filtros, aprobación y reportes. SAST inspecciona el código sin ejecutar la aplicación para detectar patrones de errores, problemas de seguridad y mantenibilidad. Son herramientas complementarias: los tests solo verifican los escenarios que se escribieron y el análisis estático tampoco encuentra todos los defectos.

**Cadena de suministro.** Una aplicación depende de librerías directas y transitivas, registros de paquetes y herramientas del pipeline. Un paquete comprometido o una cuenta de mantenimiento robada puede introducir código malicioso. Una versión legítima también puede tener vulnerabilidades conocidas; eso no implica que haya existido un ataque. Conviene auditar manifiestos como `requirements.txt` y `package.json`, sus lockfiles cuando corresponda y las acciones del CI.

**SAST y análisis de dependencias.** SonarCloud analiza nuestro código. Dependabot usa el grafo de dependencias y avisos de seguridad para detectar versiones afectadas y proponer actualizaciones. Un aviso de Dependabot no hace fallar automáticamente el Quality Gate de SonarCloud. Consultar la [configuración oficial de actualizaciones de seguridad](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates).

## Integración con SonarCloud

SonarCloud también aparece en la documentación como SonarQube Cloud. La vinculación de este proyecto ya funciona; estos son los puntos que se deben mostrar o comprobar:

1. Iniciar sesión con GitHub y seleccionar el repositorio público del equipo.
2. Elegir análisis mediante **GitHub Actions**. Si está activo el análisis automático, desactivarlo para usar el análisis del CI con cobertura.
3. Confirmar los identificadores de `sonar-project.properties`:

   ```properties
   sonar.organization=ismamati
   sonar.projectKey=ismamati_Tp_Gestion-de-Desarrollos-de-Software
   sonar.sources=app
   sonar.tests=tests
   sonar.python.coverage.reportPaths=coverage.xml
   ```

4. Guardar el token como `SONAR_TOKEN` en **Settings → Secrets and variables → Actions**. En el video, mostrar el nombre del secreto; su valor no se necesita para explicar la integración.
5. Mostrar que el workflow conserva el historial Git con `fetch-depth: 0` y genera `coverage.xml` antes del scanner.

El step existente es:

```yaml
- name: Analizar con SonarCloud
  uses: SonarSource/sonarqube-scan-action@v8
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  with:
    args: -Dsonar.qualitygate.wait=${{ github.event_name == 'pull_request' }}
```

La acción ejecuta SonarScanner. En un PR, la expresión se convierte en `true`: el scanner espera el resultado del gate y falla si el gate falla. En un push a `main`, vale `false`: se envía el análisis sin esperar el gate. Para exigir también el gate en los pushes a `main`, reemplazar el argumento por `-Dsonar.qualitygate.wait=true`. Consultar la [integración oficial con GitHub Actions](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/ci-based-analysis/github-actions-for-sonarcloud) y el [parámetro de espera](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/analysis-parameters/parameters-not-settable-in-ui).

## Quality Gate

Abrir el proyecto en SonarCloud y entrar en **Quality Gate**. Mostrar el gate asignado y sus condiciones, no solo el indicador verde o rojo.

| Métrica del código nuevo | Condición que hace fallar el gate | Resultado observado en PR #2 |
| --- | --- | --- |
| Bugs | Mayor que 0 | 0: pasa |
| Vulnerabilidades | Mayor que 0 | 0: pasa |
| Cobertura | Menor que 80% | 4,8%: falla |
| Duplicación | Mayor que 3% | 82,8%: falla |

El PR también presenta 1 Code Smell, pero la condición de mantenibilidad pasa. No afirmar que el pipeline falla por la variable sin usar: los motivos comprobados son cobertura y duplicación.

El gate gratuito **Sonar way** permite cumplir los umbrales principales de la actividad. La documentación actual reserva los gates personalizados para Team y Enterprise; no es necesario contratar un plan para usar el gate incorporado. En los PR se evalúan las condiciones sobre código nuevo. Ver la [definición oficial de Quality Gates](https://docs.sonarsource.com/sonarqube-cloud/standards/managing-quality-gates/introduction-to-quality-gates).

Por defecto, SonarCloud puede ignorar cobertura y duplicación en cambios con menos de 20 líneas nuevas. Para aplicar el requisito incluso a cambios pequeños, desmarcar **Ignore duplication and coverage on small changes** en **Quality Gate** y guardar. Es especialmente relevante después de reemplazar la función duplicada por una función breve. Ver la [configuración oficial del proyecto](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/changing-quality-gate).

La cobertura indica qué parte del código ejecutaron los tests. Un 100% de cobertura no demuestra por sí solo que todas las comprobaciones sean correctas o suficientes.

## Dependabot

El proyecto contiene `python-multipart==0.0.6`, una versión afectada por [CVE-2024-24762](https://github.com/advisories/GHSA-2jv5-9r88-3w3p). En aplicaciones que procesan formularios con esa versión, un encabezado especialmente construido puede provocar consumo excesivo de CPU y denegación de servicio. Este proyecto no usa la librería en su código de notas: sirve como ejemplo de detección de una dependencia vulnerable, sin necesidad de ejecutar un ataque.

Para verificar la configuración, abrir **Settings → Advanced Security** (en algunas interfaces, **Code security and analysis**) y comprobar:

- **Dependency graph** habilitado.
- **Dependabot alerts** habilitado.
- **Dependabot security updates** habilitado.

Mostrar el aviso en **Security → Dependabot** y el PR #1 con la actualización propuesta. La existencia del PR demuestra que hubo una actualización automática, pero conviene mostrar también el estado de las opciones.

No hace falta un `dependabot.yml` para recibir actualizaciones de seguridad. Si el equipo también quiere actualizaciones periódicas de versiones y del propio CI, puede agregar `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

Este archivo configura actualizaciones de versiones; las opciones de seguridad se habilitan en GitHub. Después de registrar la evidencia, revisar la actualización de Dependabot y sus checks antes de integrar la corrección.

## Branch Protection y bloqueo de merge

En **Settings → Branches**, editar o crear la protección de `main` que se usó en la Actividad 6:

1. Activar **Require a pull request before merging**.
2. Activar **Require status checks to pass before merging**.
3. Seleccionar los checks reales observados: `tests` de GitHub Actions y `SonarCloud Code Analysis` de la integración SonarCloud.
4. Aplicar las restricciones también a administradores con **Do not allow bypassing the above settings**, si la demostración se hace desde la cuenta administradora. Si se usa un ruleset, revisar su lista de bypass.
5. Guardar y abrir el PR #2. Mostrar el mensaje de bloqueo por checks requeridos, además de los checks rojos.

Un workflow rojo solo bloquea el merge cuando sus checks son obligatorios. La ausencia de conflictos tampoco prueba que el merge esté permitido. Si hay revisiones obligatorias u otras condiciones de la Actividad 6, deben cumplirse además del gate para habilitar el merge. Ver la [documentación de ramas protegidas](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

## Corrección del PR de demostración

El [PR #2](https://github.com/ismamati/Tp_Gestion-de-Desarrollos-de-Software/pull/2), en la rama `demo-code-smell`, agrega `reporte_aprobados` copiando casi toda la implementación de `reporte_curso` y declarando `total_inscriptos` sin usar. Los tests actuales pasan porque no comprueban la nueva función.

Después de grabar el estado rojo, trabajar sobre esa misma rama y reemplazar **la función completa** `reporte_aprobados` por:

```python
def reporte_aprobados(alumnos):
    aprobados = [alumno for alumno in alumnos if esta_aprobado(alumno)]
    return reporte_curso(aprobados)
```

Así se conserva el comportamiento esperado, se elimina la variable sin uso y se reutiliza el cálculo existente. Añadir `reporte_aprobados` al import de `tests/test_notas.py` y agregar casos que comprueben el comportamiento:

```python
def test_reporte_aprobados_filtra_y_calcula():
    assert reporte_aprobados(ALUMNOS) == {
        "cantidad": 2,
        "promedio": 8.5,
        "nombres": ["Ana", "Carla"],
        "materias": ["Historia"],
        "mejor_alumno": "Carla",
        "mejor_nota": 9,
    }


def test_reporte_aprobados_sin_aprobados():
    assert reporte_aprobados([ALUMNOS[1]]) == reporte_curso([])


def test_reporte_aprobados_incluye_nota_limite():
    alumno = {"nombre": "Diego", "materia": "Historia", "nota": 6}
    assert reporte_aprobados([alumno]) == reporte_curso([alumno])
```

Ejecutar los mismos tests del CI:

```powershell
python -m pytest --cov=app --cov-report=xml --cov-report=html
```

Hacer commit y push a `demo-code-smell`. El PR existente recibe el cambio y dispara un nuevo análisis. Comprobar la cobertura del código nuevo y los checks reales antes de grabar el estado verde. No se ejecutó esta corrección durante la preparación de la guía.

## Guion del video

| Momento aproximado | Qué mostrar | Qué explicar |
| --- | --- | --- |
| 0:00–1:00 | `app/notas.py` y tests | Deuda técnica, Code Smells y diferencia entre tests dinámicos y SAST. |
| 1:00–2:00 | Dashboard de `main` | Bugs: confiabilidad; Vulnerabilidades: seguridad del código; Code Smells: mantenibilidad; Duplicación: código repetido. Mostrar cobertura y distinguir código global de código nuevo. |
| 2:00–3:00 | Quality Gate y workflow | Umbrales de Bugs, Vulnerabilidades y cobertura; generación de `coverage.xml`; análisis después de los tests; espera del gate en PR. |
| 3:00–4:00 | Diff del PR #2 y resultado de SonarCloud | La función duplicada y la variable sin usar; tests verdes y gate rojo por 4,8% de cobertura y 82,8% de duplicación. |
| 4:00–4:45 | Checks del PR y protección de `main` | `tests` y `SonarCloud Code Analysis` obligatorios; mensaje real que impide el merge. |
| 4:45–6:00 | Corrección, tests y nuevo push en la misma rama | Reutilización de `reporte_curso`, eliminación de duplicación y tests de la nueva función. Esperar el nuevo análisis y mostrar checks verdes y merge habilitado cuando se cumplan las demás condiciones. |
| 6:00–7:00 | Security → Dependabot y PR #1 | Riesgo de librerías de terceros, vulnerabilidad conocida y actualización automática. |

Cierre sugerido: “Los tests comprueban el comportamiento, SonarCloud controla la calidad del código y Dependabot vigila las dependencias. Con checks obligatorios, GitHub exige que se cumplan estos controles antes de integrar cambios”.
