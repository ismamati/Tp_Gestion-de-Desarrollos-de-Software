# Diapositivas y notas para exponer

Presentación: jueves 15/10/2026. Completar nombres y capturas reales.

## 1. Que funcione es el comienzo

Calidad de código, deuda técnica y seguridad · DevSecOps

**Nuestra propuesta**

- Comprobar comportamiento
- Revisar calidad y seguridad
- Controlar antes de integrar

**Una demo pequeña**

- Notas de alumnos en Python
- GitHub Actions + SonarCloud
- Dependabot + protección de main

**Para explicar oralmente:** Completar los nombres del equipo. Presentamos el jueves 15 de octubre de 2026. La idea central: un cambio puede pasar los tests y aun así necesitar mejoras antes de integrarse. No afirmamos que los controles garanticen ausencia total de defectos.

## 2. ¿Qué hace la aplicación?

Un módulo Python; los datos entran como una lista de alumnos

**Tres funciones**

- Buscar alumnos por materia
- Aprobar con nota ≥ 6
- Resumir cantidad, promedio y mejor nota

**Un ejemplo concreto**

- Ana: 8 · Bruno: 4 · Carla: 9
- Aprobados: Ana y Carla
- Promedio del curso: 7,0

**Para explicar oralmente:** No es una web: no tiene pantallas, servidor ni base de datos. app/notas.py recibe datos y devuelve resultados. buscar_por_materia filtra; esta_aprobado devuelve verdadero o falso; reporte_curso devuelve un diccionario. Los cinco tests están en tests/test_notas.py. pytest corre los tests y pytest-cov mide cobertura.

## 3. La deuda aparece al mantener

Una solución rápida puede aumentar el costo del próximo cambio

**Deuda técnica**

- Copiamos el cálculo de un reporte
- Una corrección requiere cambiar dos sitios
- Más trabajo y riesgo de inconsistencias

**Code Smells**

- Variables que nunca se usan
- Funciones difíciles de entender
- Señales para revisar la mantenibilidad

**Para explicar oralmente:** Un Code Smell no significa que el programa ya falla ni que hay una vulnerabilidad. SonarCloud mide la duplicación por separado. La deuda puede ser consciente si se registra y se planifica su corrección. En nuestro PR hay una copia de reporte_curso y una variable total_inscriptos que no se utiliza.

## 4. Dos formas de revisar el código

Los tests y el análisis estático responden preguntas diferentes

**Testing dinámico**

- Ejecuta el código
- Compara resultados con lo esperado
- pytest aquí; Playwright en navegador

**Análisis estático · SAST**

- Inspecciona sin ejecutar la aplicación
- Busca patrones de errores y seguridad
- SonarCloud analiza nuestro cambio

**Para explicar oralmente:** Ejemplo: pytest llama a esta_aprobado y comprueba el resultado. SonarCloud inspecciona el código y señala patrones problemáticos. SonarCloud no ejecuta nuestros tests: Actions ejecuta pytest y SonarCloud importa coverage.xml. Ninguno de estos controles detecta todos los problemas.

## 5. También dependemos de código ajeno

La cadena de suministro incluye librerías y herramientas del CI

**Qué puede pasar**

- Una versión tiene una vulnerabilidad
- Una cuenta de publicación es comprometida
- Un paquete malicioso llega al proyecto

**Dependabot**

- Detecta versiones con avisos conocidos
- Genera alertas y propone actualizaciones
- Ya tenemos el PR #1 de python-multipart

**Para explicar oralmente:** Una vulnerabilidad conocida no prueba que haya existido un ataque. requirements.txt incluye python-multipart 0.0.6, afectado por CVE-2024-24762. El módulo de notas no lo usa; está como ejemplo. Dependabot ya propuso actualizar a 0.0.31. Una alerta de Dependabot no hace fallar automáticamente el gate de SonarCloud. Fuente: https://github.com/advisories/GHSA-2jv5-9r88-3w3p .

## 6. Qué tenemos y qué falta

Estado consultado el 13/10/2026 · comprobar antes de grabar

**Ya funciona**

- Tests y reportes de cobertura
- SonarCloud dentro del workflow
- PR #2 rojo y PR #1 de Dependabot

**Por completar**

- Verificar bloqueo real de merge
- Corregir y comprobar checks verdes
- Grabar evidencia y ensayar

**Para explicar oralmente:** La protección de main no pudo verificarse con la API pública porque requiere autenticación. No presentarla como configurada hasta comprobarla. El PR #2 está abierto y falla por el Quality Gate; el PR #1 también está abierto. La corrección verde todavía no está hecha en esta preparación.

## 7. Qué recorre cada Pull Request

GitHub Actions ejecuta la secuencia automáticamente

PR → Instalar → Tests + cobertura → SonarCloud → Gate → Merge*

**Quality Gate**

- Bugs nuevos = 0
- Vulnerabilidades nuevas = 0
- Cobertura nueva ≥ 80%

***Checks obligatorios**

- GitHub debe exigir su aprobación
- Gate rojo → check rojo → bloqueo
- Otras condiciones también se cumplen

**Para explicar oralmente:** El workflow genera coverage.xml después de ejecutar pytest. El step oficial de SonarCloud ejecuta SonarScanner y espera el gate en PR con sonar.qualitygate.wait=true. En pushes a main el workflow actual no espera el resultado del gate. La regla de duplicación observada tiene un máximo de 3%. En un PR se evalúa código nuevo. Para cambios menores de 20 líneas, desmarcar Ignore duplication and coverage on small changes en Quality Gate si se quiere exigir ese control. Fuente: https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/changing-quality-gate .

## 8. Leer el dashboard

Comparar el código global con el código nuevo del PR

**Problemas detectados**

- Bugs → confiabilidad
- Vulnerabilidades → seguridad
- Code Smells → mantenibilidad

**Otras métricas**

- Duplicación → bloques repetidos
- Cobertura → código ejecutado en tests
- 100% no prueba todos los escenarios

**Para explicar oralmente:** Mostrar el dashboard real y la configuración del gate. Para main se consultaron cobertura global de 100%, cero Bugs, Vulnerabilidades y Code Smells, y duplicación de 0%. No mezclar estas métricas con las del PR. Abrir https://sonarcloud.io/dashboard?id=ismamati_Tp_Gestion-de-Desarrollos-de-Software .

## 9. La demo roja ya está preparada

PR #2 · Agrego reporte de aprobados

**Qué ocurre**

- Se copia el cálculo del reporte
- Los tests antiguos siguen pasando
- La función nueva casi no se ejecuta

**Resultado comprobado**

- Cobertura nueva: 4,8% < 80%
- Duplicación: 82,8% > 3%
- Quality Gate: ERROR

**Captura pendiente:** Agregar captura real: gate rojo + checks + merge bloqueado

**Para explicar oralmente:** Abrir https://github.com/ismamati/Tp_Gestion-de-Desarrollos-de-Software/pull/2 . Se detectó también un Code Smell, pero la condición de mantenibilidad pasa: no atribuir el fallo a la variable sin usar. Los motivos comprobados son cobertura y duplicación. Mostrar el diff y luego los checks. Registrar la evidencia roja antes de modificar la rama. El bloqueo de merge necesita checks obligatorios.

## 10. La corrección cabe en tres líneas

Filtrar los aprobados y reutilizar el reporte existente

```python
def reporte_aprobados(alumnos):
    aprobados = [a for a in alumnos if esta_aprobado(a)]
    return reporte_curso(aprobados)
```

**Qué mejora**

- Un solo cálculo para mantener
- Sin la variable que no se usa
- Mismo objetivo funcional

**Qué pruebo**

- Ana y Carla: promedio 8,5
- Sin aprobados: reporte vacío
- Una nota de 6 también aprueba

**Para explicar oralmente:** Usar la misma rama demo-code-smell del PR #2. Reemplazar toda la función copiada por estas líneas y agregar tests a tests/test_notas.py. Ejecutar pytest con cobertura, hacer commit y push. El código usa a como nombre corto en pantalla; la guía usa alumno para mayor claridad. No editar main para corregir un PR.

## 11. Cerrar el ciclo con evidencia

El resultado verde debe comprobarse después del nuevo push

**En GitHub y SonarCloud**

- Mismo PR, nuevo commit
- Tests y gate aprobados
- Merge permitido al cumplir requisitos

**En Dependabot**

- Mostrar la alerta de seguridad
- Mostrar la versión propuesta en PR #1
- Revisar checks antes de integrar

**Captura pendiente:** Agregar captura real del nuevo análisis verde y del PR de Dependabot

**Para explicar oralmente:** Esta diapositiva describe el resultado pendiente, no uno que ya se haya producido. Verificar tests y SonarCloud Code Analysis verdes. Si siguen pendientes revisiones, conversaciones u otras condiciones, el merge puede continuar bloqueado. No usar bypass. Configurar la protección para aplicar a administradores si presentan desde esa cuenta. Dependabot: Settings → Advanced Security → Dependency graph, alerts y security updates. Fuente: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates .

## 12. Cada control responde una pregunta

Automatizar la revisión para integrar mejores cambios

**Antes de integrar**

- Tests: ¿se comporta como esperamos?
- SonarCloud: ¿cumple calidad y seguridad?
- Dependabot: ¿hay versiones vulnerables?

**Lo que demostramos**

- El rojo tiene un motivo concreto
- La corrección mejora código y tests
- GitHub exige los checks configurados

**Para explicar oralmente:** Cerrar con la idea de que calidad y seguridad forman parte del flujo habitual de desarrollo. Preparar respuestas: cobertura no equivale a ausencia de Bugs; un smell no es una vulnerabilidad; SonarCloud y Dependabot tienen funciones diferentes; un check rojo solo bloquea si es obligatorio. El archivo GUIA_EQUIPO.md tiene el procedimiento detallado y una alternativa pequeña llamada contar_aprobados.
