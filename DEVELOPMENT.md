# Evolución del Proyecto ETL

## Semana 1 — Exploración y entendimiento del dominio de datos

### Enfoque técnico
Trabajo inicial basado en notebooks (notebooks/01_carga_datos.ipynb) utilizando pandas para exploración y procesamiento manual de datos contables.

### Decisiones técnicas
- Uso de notebooks como entorno principal de análisis exploratorio.
- Implementación de limpieza manual de datos:
Normalización de nombres de columnas.
Transformación de formatos de fecha.
nonimización de datos sensibles.

- Ausencia de arquitectura modular o separación de capas.

### Limitaciones identificadas.
- Lógica no reutilizable ni escalable
- Mezcla de responsabilidades (carga, transformación y validación en un solo entorno).
- Dificultad para mantenimiento y reproducción del proceso.

### Resultado técnico
* Se identifican problemas reales de datos contables en Excel:
- Inconsistencias de estructura.
- Variabilidad en columnas.
- Necesidad de validaciones de esquema.
- Requerimiento de un pipeline reproducible y escalable.

## Semana 2 — Migración a arquitectura modular ETL

### Arquitectura implementada
- Transición desde notebooks hacia estructura modular:
src/ ├── config.py ├── ingestion/extract.py (load_file) ├── main.py

### Decisiones técnicas
* Centralización de configuración:
- Creación de config.py para gestión de rutas.
- Eliminación de rutas hardcodeadas.

* Abstracción del proceso de ingestión:
- Implementación de load_file() como unidad central de carga.
- Separación entre lógica de carga y análisis exploratorio.

* Validaciones iniciales de datos:
- Verificación de existencia de archivo.
- Validación de formato soportado.
- Control de archivos vacíos o sin datos útiles.

* Introducción de logging básico:
- Sustitución progresiva de print() por logging.
- Inicio de trazabilidad del pipeline.

* Feedback técnico externo:
Basado en recomendaciones de la comunidad de Data Engineering, se identificó que para datos contables:

- Los archivos Excel presentan alta variabilidad estructural.
- Los esquemas cambian frecuentemente.
- Es necesario separar ingestión, validación y transformación.

### Decisión arquitectónica
Adopción de un enfoque ETL modular en lugar de un workflow basado exclusivamente en notebooks.

### Resultado técnico
Pipeline ETL funcional con capacidad de cargar ~252k filas en formato Excel con validaciones básicas.

## Semana 3 — Arquitectura Medallion y reestructuración del proyecto

### Arquitectura implementada
* Adopción de modelo Medallion:
- data/ ├── bronze/ ├── silver/ ├── gold/

- Organización adicional por dominio:
accounting/, inventory/, manufacturing/

### Decisiones técnicas clave
* Implementación de arquitectura Medallion:

- Bronze: datos crudos sin transformación.
- Silver: datos limpios y estandarizados (en desarrollo).
- Gold: datos listos para análisis (pendiente).

### Justificación:
- Estándar ampliamente utilizado en ingeniería de datos moderna.
- Adecuado para datos contables con alta variabilidad estructural.

* Fortalecimiento de la capa de ingestión:

- Validación de esquema por tipo de dataset.
- Detección de columnas faltantes en archivos estructurados incorrectamente.
- Manejo de archivos corruptos o mal formateados.
- Incorporación de type hints para mejorar mantenibilidad.

* Reestructuración del proyecto:
- Separación funcional en módulos:
ingestion/, transformations/, validations/, utils/, orchestration/

- Objetivo: simular una arquitectura de ingeniería de datos aplicada a un entorno real.

### Resultado técnico actual
El sistema permite:

- Ingestión de archivos Excel reales de gran volumen (~252k filas).
- Manejo de errores comunes en entornos contables:
- Archivos inexistentes.
- Formatos inválidos.
- Archivos vacíos.
- Esquemas inconsistentes.
- Logging básico centralizado.
- Separación clara de responsabilidades.
- Arquitectura escalable basada en capas (Medallion).

## Semana 4 — Logging centralizado, validaciones iniciales y consolidación de Silver Layer

### Implementación inicial del sistema de logging

#### Decisiones técnicas

* Implementación de sistema de logging estándar en Python para trazabilidad del pipeline ETL.
* Creación de logger centralizado (`etl_pipeline`) para registrar eventos, errores, validaciones y estado general del pipeline.
* Eliminación progresiva de `print()` dentro del flujo principal de procesamiento.
* Configuración de logging con salida a consola y archivo (`pipeline.log`) para auditoría, debugging y trazabilidad de ejecución.
* Configuración de `propagate = False` para evitar duplicación de logs entre handlers.

#### Validación de estructura del proyecto

Se validó la separación de responsabilidades dentro de la arquitectura del proyecto:

* `config.py`

  * configuración centralizada de rutas, dominios y archivos fuente.

* `logger.py`

  * configuración y trazabilidad centralizada del pipeline ETL.

* `src/ingestion/extract.py`

  * ingestión desacoplada y reutilizable por tipo de archivo.

* `src/utils/cleaning.py`

  * limpieza reutilizable para Silver Layer.

* `src/validations/general_quality.py`

  * validaciones estructurales y controles generales de calidad de datos.

* `src/validations/business_rules.py`

  * validaciones financieras y reglas de negocio contables.

* `src/orchestration/run_pipeline.py`

  * integración inicial del flujo extract → clean → validate → export.

#### Objetivo del sistema de logging

Garantizar trazabilidad consistente en entornos reproducibles, facilitando:

* debugging del pipeline
* monitoreo de errores
* auditoría básica
* validación del flujo ETL
* seguimiento de validaciones financieras
* trazabilidad de datasets procesados

---

## Robustecimiento de ingestión (Bronze Layer)

### Objetivo

Construcción de una capa de ingestión reutilizable, extensible, desacoplada y preparada para testing automatizado.

### Componentes implementados

#### Implementación de `load_file()`

Función genérica desacoplada del dataset específico.

#### Capacidades implementadas

* soporte para:

  * `.xlsx`
  * `.csv`
  * `.txt`

* validación de:

  * existencia de archivo
  * archivos vacíos
  * formatos no soportados
  * columnas mínimas requeridas

* logging automático de:

  * archivo cargado
  * cantidad de filas
  * cantidad de columnas
  * errores de ingestión

* manejo explícito de excepciones mediante:

  * `raise`
  * `FileNotFoundError`
  * `ValueError`

* eliminación de retornos silenciosos (`None`)

#### Validación mínima por tipo de dataset

Implementación de:

REQUIRED_COLUMNS

para validar columnas críticas según tipo de archivo:

* `libro_mayor`
* `inventario`
* `ordenes`

#### Funciones específicas desacopladas

Implementación de wrappers específicos:

* load_libro_mayor()
* load_movimientos_inventario()
* load_ordenes_fabricacion()

Cada función delega el procesamiento hacia `load_file()` manteniendo reutilización y separación de responsabilidades.

#### Validaciones estructurales implementadas

* validación de columnas obligatorias mediante:

  * `validate_required_columns()`

* detección inicial de:

  * columnas vacías
  * tipos inesperados
  * duplicados estructurales

---

## Construcción inicial de Silver Layer reutilizable

### Objetivo

Inicio de construcción de una capa Silver genérica orientada a limpieza reutilizable para datasets financieros y contables.

### Decisiones arquitectónicas

El diseño del pipeline fue guiado por principios comunes de Data Engineering:

* modularidad
* trazabilidad
* control básico de calidad
* separación por capas (`Bronze/Silver/Gold`)
* reutilización de lógica común
* desacoplamiento entre limpieza y validaciones financieras

### Componentes implementados

* Creación de `src/utils/cleaning.py` como módulo central de limpieza reutilizable.

* Implementación de pipeline principal:

  * `clean_dataframe(df, file_type=None)`

* Separación modular de responsabilidades mediante funciones independientes:

  * `normalize_column_names()`
  * `clean_strings()`
  * `handle_nulls()`

### Reglas generales implementadas

* Normalización de nombres de columnas:

  * eliminación de espacios
  * conversión a minúsculas
  * reemplazo de espacios por `_`
  * eliminación de caracteres especiales

* Limpieza de columnas tipo string.

* Eliminación de espacios innecesarios en texto.

* Estandarización básica de valores nulos:

  * `""`
  * `"null"`
  * `"n/a"`
  * `"none"`
    → convertidos a `pd.NA`

* Logging de limpieza por dataset usando logger centralizado.

* Registro automático de:

  * filas iniciales
  * columnas iniciales
  * filas finales
  * columnas finales

### Validación sobre dataset real

Se realizó prueba funcional utilizando el archivo:

libro_mayor_2025.xlsx

Durante la prueba se identificó que el encabezado real del archivo no se encontraba en la primera fila del Excel, por lo que fue necesario ajustar:

header=2

para realizar una lectura correcta de las columnas.

La prueba permitió:

* validar lectura de archivos Excel reales
* inspeccionar columnas, tipos de datos y valores nulos
* probar comportamiento del pipeline sobre datos financieros reales
* verificar integración entre ingestión, limpieza y logging
* procesar más de 250k registros financieros en entorno controlado

### Ajuste técnico durante pruebas

Durante la prueba inicial del pipeline sobre el archivo:

libro_mayor_2025.xlsx

el manejo de valores nulos utilizaba inicialmente:

df.applymap(_replace)

La intención era recorrer todo el DataFrame para convertir representaciones comunes de nulos (`""`, `"null"`, `"n/a"`, `"none"`) en `pd.NA`.

Sin embargo, esta estrategia generaba operaciones innecesarias sobre datasets grandes y afectaba columnas numéricas que no requerían limpieza.

Como ajuste técnico, la lógica fue refactorizada para:

* detectar dinámicamente columnas tipo `object/string`
* aplicar limpieza únicamente sobre columnas texto
* preservar columnas numéricas intactas
* reducir operaciones innecesarias sobre el DataFrame

La nueva implementación utiliza:

```python id="b1uxm0"
df[col].apply(...)
```

sobre columnas string seleccionadas dinámicamente.

---

## Construcción inicial de validaciones financieras y testing automatizado

### Objetivo

Separar validaciones estructurales, reglas financieras y testing automatizado para fortalecer robustez y mantenibilidad del pipeline.

### Componentes implementados

#### `src/validations/general_quality.py`

Implementación inicial de validaciones estructurales generales:

* validación de columnas obligatorias
* detección de columnas vacías
* validación preliminar de tipos
* detección de duplicados

#### `src/validations/business_rules.py`

Inicio de construcción de reglas financieras reutilizables:

* `validate_required_columns()`
* `validate_debe_haber()`

#### Validaciones financieras implementadas

* validación básica Debe = Haber
* tolerancia mínima para diferencias de redondeo
* logging automático de validaciones exitosas
* detección inicial de inconsistencias financieras

#### Testing automatizado inicial

Implementación inicial mediante:

pytest

#### Cobertura actual

* `tests/test_extract.py`
* validación de:

  * carga correcta de CSV
  * carga correcta de Excel
  * `FileNotFoundError`
  * formatos inválidos
  * archivos vacíos

#### Datasets dummy reproducibles

Implementación de:

scripts/generate_dummy_data.py

para creación automática de datasets de prueba determinísticos:

* `bronze_test.csv`
* `bronze_test.xlsx`
* `bronze_test_missing.xlsx`
* `bronze_test_unbalanced.xlsx`

### Estado actual del sistema

Pipeline ETL modular funcional con:

* Arquitectura Medallion implementada.

* Ingestión desacoplada y extensible.

* Soporte multi-formato:

  * Excel
  * CSV
  * TXT

* Validación básica de calidad de datos.

* Logging centralizado.

* Limpieza reutilizable.

* Normalización de columnas.

* Limpieza de strings.

* Manejo básico de nulos.

* Validaciones financieras iniciales.

* Manejo explícito de errores.

* Pruebas sobre datasets financieros reales.

* Procesamiento validado sobre más de 250k registros.

* Estructura modular orientada a producción ligera.

* Base preparada para testing automatizado con pytest.

* Integración inicial del flujo ETL reusable.

---

## En construcción

## Semana 5–6 — Consolidación de testing y estabilización inicial de Silver Layer

### Objetivo real

Fortalecer la robustez técnica del pipeline y cerrar correctamente la primera versión estable de Silver Layer para el dominio contable principal.

### Prioridad principal

#### Testing automatizado

Implementación de:

- `tests/test_cleaning.py`
- `tests/test_validations.py`

Ampliando coverage sobre:

- `cleaning.py`
- `general_quality.py`
- `business_rules.py`

### Validaciones prioritarias reales

#### Accounting

Implementación y fortalecimiento de:

- `validate_valid_dates()`
- `validate_no_negative_amounts()`
- `validate_required_columns()`
- `validate_debe_haber()`

Además de:

- validación de cuentas contables
- detección de balances inconsistentes
- validación de filas incompletas
- validación de tipos numéricos financieros

### Mejoras necesarias sobre libro mayor

- normalización robusta de fechas
- limpieza de espacios invisibles
- manejo de cuentas nulas
- validación de encabezados desplazados
- tratamiento de movimientos contables relacionados
- estabilización de columnas inconsistentes

### Expansión de datasets dummy

Fortalecimiento de:

`scripts/generate_dummy_data.py`

para cubrir escenarios como:

- fechas inválidas
- montos negativos
- balances incorrectos
- columnas faltantes
- formatos corruptos

### Resultado esperado

Silver Layer suficientemente robusta, testeable y estable para iniciar integración formal del pipeline.

---

## Semana 7–8 — Integración formal y estabilización del pipeline ETL reusable

### Objetivo real

Construir la primera versión integrada, desacoplada y estable del flujo ETL reusable sobre los 3 dominios reales.

### Prioridades

#### Integración formal del flujo

Consolidar:

extract → clean → validate → export

mediante:

- `run_pipeline.py`
- logging integrado
- validaciones desacopladas
- exportación automatizada inicial

### Robustez requerida

#### Accounting

- validaciones financieras más profundas
- validación de tipos numéricos
- trazabilidad de inconsistencias
- manejo de errores críticos

#### Inventory

- normalización de productos
- validación de cantidades
- consistencia de referencias

#### Manufacturing

- eliminación de columnas irrelevantes
- validación de estados
- limpieza básica operacional

### Refactorización inicial

- eliminación de lógica repetida
- centralización de funciones reutilizables
- separación estricta entre:
  - limpieza
  - validaciones
  - reglas financieras
  - exportación

### Resultado esperado

Pipeline reusable estable ejecutándose correctamente sobre datasets heterogéneos.

---

## Semana 9–10 — Consolidación avanzada del dominio financiero

### Objetivo real

Profundizar las validaciones financieras y estabilizar completamente el dominio contable antes de iniciar Gold Layer.

### Prioridad principal

#### Accounting

Implementación avanzada de:

- validaciones contables más profundas
- validación de cuentas obligatorias
- validación de movimientos relacionados
- detección de inconsistencias financieras
- trazabilidad de errores contables
- validación de integridad financiera

### Limpieza financiera avanzada

- normalización de cuentas contables
- manejo de registros huérfanos
- validación avanzada de fechas
- control de registros duplicados
- consolidación de formatos financieros

### Robustez del pipeline

- ampliación de testing financiero
- estabilización de exportaciones
- pruebas sobre datasets completos
- validaciones cruzadas básicas

### Resultado esperado

Dominio financiero suficientemente sólido y estable para iniciar construcción analítica real.

---

## Semana 11–12 — Consolidación de inventory y manufacturing

### Objetivo real

Preparar datasets operativos suficientemente limpios y consistentes para integrarlos correctamente a Gold Layer.

### Inventory

Implementación de:

- validación de cantidades
- consistencia de referencias
- movimientos entre bodegas
- limpieza de productos inconsistentes
- validación de fechas operativas
- detección de registros anómalos

### Manufacturing

Implementación de:

- validación de órdenes
- limpieza de estados
- validación de cantidades producidas
- detección de registros incompletos
- consolidación operativa básica

### Resultado esperado

Datasets operativos suficientemente estables para análisis y consolidación analítica.

---

## Semana 13–14 — Construcción inicial de Gold Layer

### Objetivo real

Construir datasets analíticos limpios, estables y realmente consumibles para BI y SQL.

### Datasets prioritarios

#### `financial_summary`

Debe incluir:

- movimientos contables limpios
- agregaciones por período
- cuentas contables
- débitos/créditos
- balances
- métricas financieras básicas

#### `inventory_summary`

Debe incluir:

- movimientos por producto
- entradas/salidas
- movimientos entre bodegas
- cantidades consolidadas

#### `production_summary`

Debe incluir:

- órdenes por estado
- cantidades producidas
- actividad operativa básica

### Construcción técnica

Implementación de:

- `data/gold/`
- `src/gold/exporter.py`

Exportación en:

- Parquet
- CSV

### Validaciones analíticas

- consistencia entre Silver y Gold
- validación de balances
- integridad de métricas
- validación de agregaciones

### Resultado esperado

Primer entorno Gold reusable listo para SQL y Power BI.

---

## Semana 15–16 — SQL analítico financiero (Parte 1)

### Objetivo real

Comenzar consumo analítico real sobre datasets Gold utilizando SQL financiero.

### Prioridad absoluta

#### `financial_summary`

Implementación de:

- agregaciones
- `GROUP BY`
- joins
- filtros analíticos
- validaciones cruzadas
- métricas financieras iniciales

### KPIs financieros iniciales

- total débitos
- total créditos
- movimientos por período
- cuentas más utilizadas
- variaciones mensuales básicas

### Resultado esperado

Primer entorno SQL funcional orientado a análisis financiero.

---

## Semana 17–18 — SQL analítico financiero (Parte 2)

### Objetivo real

Profundizar SQL analítico y comenzar construcción formal de KPIs financieros reutilizables.

### SQL intermedio/avanzado

Implementación de:

- CTEs
- subqueries
- window functions
- acumulados
- rankings financieros
- análisis temporales

### Validaciones analíticas

- integridad financiera
- validación de balances
- consistencia entre datasets
- validación de métricas agregadas

### Resultado esperado

Modelo SQL más sólido y orientado a Finance BI.

---

## Semana 19–20 — Construcción de KPIs financieros y operativos

### Objetivo real

Transformar datasets Gold en métricas financieras y operativas reutilizables.

### KPIs financieros

#### Accounting

- crecimiento mensual
- variaciones contables
- tendencias financieras
- comportamiento operativo
- movimientos relevantes

#### Inventory

- rotación
- movimientos
- referencias más utilizadas

#### Manufacturing

- órdenes procesadas
- estados operativos
- cantidades producidas

### Resultado esperado

KPIs financieros y operativos listos para consumo BI.

---

## Semana 21–22 — Construcción inicial de dashboards en Power BI

### Objetivo real

Conectar datasets Gold y KPIs a Power BI para construir las primeras visualizaciones financieras reales.

### Dashboards prioritarios

#### Finanzas

- balances
- movimientos
- tendencias
- variaciones
- KPIs financieros

#### Inventario

- entradas/salidas
- movimientos
- referencias

#### Producción

- órdenes
- estados
- actividad operativa

### Resultado esperado

Primer entorno BI funcional conectado directamente al pipeline.

---

## Semana 23–24 — Consolidación analítica y validación BI

### Objetivo real

Validar consistencia entre SQL, KPIs y dashboards antes de profesionalizar el proyecto.

### Prioridades

- validación de métricas visuales
- consistencia entre SQL y Power BI
- validación de KPIs
- revisión de filtros y agregaciones
- estabilización de dashboards

### Resultado esperado

Entorno BI estable y consistente.

---

## Semana 25–26 — Consolidación arquitectónica y optimización

### Objetivo real

Reducir redundancia, mejorar mantenibilidad y estabilizar completamente la arquitectura reusable.

### Prioridades

#### Refactorización general

- revisión completa del pipeline
- eliminación de lógica duplicada
- unificación de reglas similares
- simplificación de transformaciones

#### Optimización técnica

- optimización de validaciones
- mejora de performance sobre datasets grandes
- reducción de operaciones innecesarias
- mejora de trazabilidad

#### Consolidación reusable

Centralización de lógica común en:

- `cleaning.py`
- `general_quality.py`
- `business_rules.py`
- helpers reutilizables

### Resultado esperado

Pipeline financiero robusto, mantenible y profesional.

---

## Semana 27–28 — Storytelling técnico y profesionalización del proyecto

### Objetivo real

Convertir el proyecto completo en un caso de estudio sólido para Finance BI y Financial Data Analytics.

### Implementaciones

#### README profesional

Documentación de:

- arquitectura Medallion
- flujo ETL
- validaciones financieras
- datasets Gold
- KPIs
- dashboards
- ejemplos de ejecución

#### Storytelling financiero

- hallazgos relevantes
- decisiones técnicas
- problemas detectados
- impacto analítico
- evolución del pipeline

#### Preparación profesional

- screenshots
- diagramas
- explicación técnica
- explicación funcional
- narrativa para entrevistas
- optimización GitHub y LinkedIn

### Resultado esperado

Proyecto completamente documentado, explicable y listo para portafolio profesional.