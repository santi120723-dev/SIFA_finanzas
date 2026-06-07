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

## Semana 5 — Sistema de Validaciones Financieras

### Objetivo

Implementar un sistema de validaciones reutilizable que permita detectar errores estructurales y financieros antes de que los datos continúen hacia etapas posteriores del pipeline.

### ✅ LO QUE YA TIENES HECHO HOY

#### Sistema base de validaciones consolidado

Ya implementaste correctamente la estructura principal de validaciones:

src/validations/severity.py

src/validations/generic_validations.py

src/validations/business_rules.py

src/validations/validation_runner.py

src/validations/warning_validations.py

✔ La capa de validaciones ya se encuentra integrada y funcionando dentro del proyecto.


#### Severidades definidas e integradas

Actualmente el sistema contempla:

* WARNING funcionando

* INFO preparado conceptualmente

* CRITICAL implementado

✔ Las validaciones críticas ya pueden detener la ejecución cuando se detectan errores que comprometen la calidad o consistencia de la información.

#### Validation runner funcional

* ejecución centralizada mediante run_validations()
* separación entre validaciones críticas y advertencias
* estructura extensible para futuras reglas
* retorno estructurado de resultados

✔ El motor de validaciones ya está operativo y desacoplado de las reglas específicas.

#### Validaciones CRITICAL implementadas

Actualmente existen validaciones críticas funcionales:

* validate_required_columns()
* validate_dates()
* validate_debe_haber()

✔ El sistema ya puede detectar errores estructurales y contables antes de que los datos continúen en el flujo de procesamiento.

#### Validaciones WARNING funcionando

Actualmente existen validaciones de advertencia como:

* validate_nulls()
* validate_empty_dataframe()
* validate_duplicates()

✔ El sistema ya genera alertas de calidad de datos sin interrumpir la ejecución.

#### Integración con pipeline

Ya lograste:

* conectar run_validations(cleaned_df)
* ejecutar validaciones después del proceso de limpieza
* mantener compatibilidad con run_pipeline()
* mantener la arquitectura desacoplada

✔ El pipeline puede ejecutar validaciones automáticamente dentro del flujo ETL.

#### Separación arquitectónica lograda

Actualmente existe una separación clara entre:

* ingestion → carga
* cleaning → limpieza y estandarización
* validations → control de calidad y reglas de negocio

✔ La arquitectura permite seguir creciendo sin mezclar responsabilidades.

#### Reutilización de validaciones

Ya se implementó:

generic_validations.py

con reglas reutilizables como:

* validate_required_columns()
* validate_dates()

✔ La lógica común ya no depende exclusivamente del dominio contable y puede reutilizarse en futuros datasets.

#### Pruebas automatizadas implementadas

Ya existen pruebas con pytest para:

* columnas obligatorias
* fechas inválidas
* fechas nulas
* desbalance contable
* duplicados

✔ Las validaciones principales ya cuentan con cobertura básica de pruebas automatizadas.

#### Datasets de prueba creados

Actualmente existen datasets de prueba como:

* critical_imbalanced.csv
* critical_imbalanced2.csv
* missing_columns.csv
* invalid_dates.csv
* null_dates.csv
* duplicates.csv
* no_duplicates.csv

✔ Ya existe una base reproducible para validar el comportamiento del sistema.

---

### ⚠️ LO QUE TE FALTA POR HACER

#### Nuevas validaciones financieras

Aún faltan reglas orientadas a calidad y consistencia como:

* validate_data_types()
* validate_value_ranges()
* validaciones específicas por dominio

❌ Todavía no existe cobertura para estos escenarios.

#### Evolución de business_rules.py

Actualmente contiene reglas contables básicas.

Falta incorporar:

* reglas financieras adicionales
* reglas específicas de inventario
* reglas específicas de fabricación
* validaciones de negocio más complejas

❌ La capa de reglas de negocio aún puede crecer significativamente.

#### Selección de validaciones por dominio

Actualmente todas las validaciones se ejecutan de forma global.

Falta implementar:

* asociación dominio → validaciones
* ejecución contextual según tipo de dataset
* registro de validaciones por dominio

❌ Todavía no existe separación dinámica de reglas.

#### Logging más estructurado

Actualmente ya existen logs funcionales.

Falta evolucionar hacia:

* mayor granularidad por severidad
* métricas de validación
* reportes consolidados de ejecución
* trazabilidad ampliada

❌ Aún hay margen de mejora para observabilidad.

#### Cobertura de pruebas

Actualmente existen pruebas básicas.

Falta incorporar:

* tests de tipos de datos
* tests de rangos
* tests de integración completos

❌ La cobertura todavía puede ampliarse.

#### Preparación para nuevos dominios

La arquitectura ya permite crecer.

Falta implementar:

* validaciones de inventario
* validaciones de órdenes de fabricación
* catálogo de reglas por dominio

❌ La estructura está preparada, pero los nuevos dominios aún no han sido desarrollados.

---

## Semana 6 — Integración del Pipeline y Consolidación de Silver Layer

### Objetivo

Construir el primer flujo ETL completo reutilizable:

Bronze → Clean → Validate → Silver

dejando una Silver Layer estable y lista para futuras transformaciones analíticas.

### Prioridad Principal

#### Integración formal del pipeline

Consolidar:

* load_file()
* clean_dataframe()
* run_validations()
* run_pipeline()

mediante:

* src/orchestration/run_pipeline.py

✔ La base funcional del pipeline ya existe y será fortalecida durante esta etapa.

### Flujo objetivo

#### Pipeline Silver

Bronze

↓

load

↓

clean

↓

validate

↓

save_silver

### Archivos prioritarios

* src/orchestration/run_pipeline.py
* src/utils/export_silver.py
* data/silver/accounting/
* tests/

### Exportación Silver

#### Persistencia de datasets limpios

Implementar:

* export_silver()
* exportación Parquet
* creación automática de rutas
* trazabilidad de archivos exportados

### Testing prioritario

#### Integración

Implementar:

* test_pipeline_integration.py

Validando:

* carga correcta
* limpieza correcta
* validaciones ejecutadas
* generación correcta de archivos Silver

### Validaciones adicionales

#### Calidad del dato

Implementar:

* validate_data_types()
* validate_value_ranges()

#### Reutilización

Diseñar validaciones para que puedan utilizarse en:

* accounting
* inventory
* manufacturing

### Resultado esperado

Primer pipeline ETL completo ejecutando:

Bronze → Silver

- de forma automatizada, reutilizable y preparada para futuras transformaciones analíticas.

La Silver Layer quedará lista para soportar la construcción posterior de datasets analíticos en Gold Layer.


---

## Semana 7–8 — Integración formal y estabilización del pipeline ETL reusable

### Objetivo real

Construir la primera versión integrada, desacoplada y estable del flujo ETL reusable sobre los 3 dominios reales.

### Prioridades

#### Integración formal del flujo

Consolidar:

extract → clean → validate → export

mediante:

- run_pipeline.py
- logging integrado
- validaciones desacopladas
- exportación automatizada inicial

### Robustez requerida

#### Accounting

Implementar:

- reglas financieras adicionales
- validaciones de integridad financiera
- validaciones de tipos numéricos
- trazabilidad de inconsistencias

#### Inventory

Implementar:

- normalización de productos
- validación de cantidades
- consistencia de referencias

#### Manufacturing

Implementar:

- limpieza de columnas irrelevantes
- validación de estados
- normalización básica operacional

### Refactorización inicial

#### Reutilización

Consolidar:

- generic_validations.py
- business_rules.py

Reduciendo:

- lógica duplicada
- validaciones repetidas
- código específico difícil de reutilizar

### Testing e integración

#### Validación integral

Ejecutar pruebas sobre:

- datasets contables
- datasets de inventario
- datasets de manufactura

Verificando:

- validaciones
- exportaciones
- estabilidad del pipeline

### Resultado esperado

Pipeline reusable estable ejecutándose correctamente sobre datasets heterogéneos y preparado para iniciar consolidación avanzada por dominio.

## Semana 9–10 — Consolidación avanzada del dominio financiero

### Objetivo real

Profundizar las validaciones financieras y estabilizar completamente el dominio contable antes de iniciar la construcción formal de la Gold Layer.

### Prioridad principal

#### Fortalecimiento del dominio Accounting

Implementar validaciones más robustas sobre:

- cuentas contables
- movimientos financieros
- integridad de registros
- consistencia estructural
- calidad del dato financiero

#### Reglas financieras avanzadas

Incorporar validaciones como:

- cuentas obligatorias
- movimientos inconsistentes
- registros incompletos
- detección de anomalías financieras
- validaciones cruzadas básicas

### Calidad y confiabilidad del dato

#### Limpieza financiera avanzada

Implementar:

- normalización de cuentas contables
- control de registros duplicados
- validación avanzada de fechas
- validación de campos obligatorios
- estandarización de formatos financieros

#### Trazabilidad

Fortalecer:

- logging financiero
- identificación de errores
- monitoreo de validaciones
- auditoría básica de ejecución

### Robustez del pipeline

#### Testing financiero

Ampliar cobertura mediante:

- datasets más grandes
- escenarios de error financiero
- validaciones cruzadas
- pruebas de integración

#### Estabilidad operativa

Validar:

- ejecución continua del pipeline
- comportamiento ante errores críticos
- comportamiento ante warnings
- consistencia de exportaciones

### Resultado esperado

Dominio financiero suficientemente sólido, confiable y estable para soportar procesos analíticos y futuras capas de consumo BI.

---

## Semana 11–12 — Consolidación de Inventory y Manufacturing

### Objetivo real

Preparar datasets operativos suficientemente limpios y consistentes para integrarlos correctamente a futuras capas analíticas.

### Prioridad principal

#### Dominio Inventory

Implementar:

- validación de cantidades
- consistencia de referencias
- control de valores nulos
- detección de registros duplicados
- normalización de productos

#### Calidad operativa

Validar:

- entradas y salidas
- movimientos entre ubicaciones
- registros incompletos
- formatos inconsistentes

### Dominio Manufacturing

#### Limpieza operacional

Implementar:

- validación de órdenes
- limpieza de estados
- normalización de campos operativos
- detección de registros incompletos

#### Consistencia de producción

Validar:

- cantidades producidas
- fechas operativas
- estados inconsistentes
- registros duplicados

### Reutilización del framework de validaciones

#### Aplicación de reglas genéricas

Extender:

- validate_required_columns()
- validate_dates()
- validate_duplicates()
- validaciones de tipos

a:

- inventory
- manufacturing

### Testing

#### Cobertura operativa

Implementar:

- datasets de inventario
- datasets de manufactura
- pruebas de validaciones específicas
- pruebas de integración

### Resultado esperado

Datasets operativos suficientemente estables para iniciar procesos analíticos y consolidación posterior en Gold Layer.

---

## Semana 13–14 — Construcción inicial de Gold Layer

### Objetivo real

Construir datasets analíticos limpios, consistentes y consumibles para SQL y Business Intelligence.

### Prioridad principal

#### Diseño de Gold Layer

Crear:

- data/gold/
- estructura de exportación analítica
- datasets agregados
- primeras métricas consolidadas

### Datasets prioritarios

#### financial_summary

Debe incluir:

- movimientos contables limpios
- agregaciones por período
- débitos y créditos
- balances básicos
- métricas financieras iniciales

#### inventory_summary

Debe incluir:

- movimientos por producto
- entradas y salidas
- cantidades consolidadas
- comportamiento operativo básico

#### production_summary

Debe incluir:

- órdenes por estado
- cantidades producidas
- actividad operacional consolidada

### Construcción técnica

#### Exportación

Implementar:

- exportación Parquet
- exportación CSV
- control de versiones básicas de datasets

#### Validaciones analíticas

Verificar:

- consistencia entre Silver y Gold
- integridad de métricas
- calidad de agregaciones
- ausencia de registros inconsistentes

### Preparación para BI

#### Consumo analítico

Diseñar datasets pensando en:

- SQL
- Power BI
- reporting financiero
- análisis operativo

### Resultado esperado

Primera versión funcional de la Gold Layer lista para consumo analítico.

---

## Semana 15–16 — SQL Analítico Financiero (Parte 1)

### Objetivo real

Comenzar el consumo analítico real de los datasets Gold mediante SQL, construyendo consultas financieras orientadas a reporting y análisis de negocio.

### Prioridad principal

#### Dominio financiero

Implementar consultas sobre:

- financial_summary
- métricas financieras básicas
- balances consolidados
- movimientos contables

### SQL fundamental

#### Consultas analíticas

Implementar:

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- HAVING
- JOIN básicos

### Métricas financieras iniciales

#### Indicadores básicos

Construir consultas para:

- total débitos
- total créditos
- movimientos por período
- movimientos por cuenta
- variaciones mensuales básicas

### Validaciones analíticas

#### Consistencia financiera

Verificar:

- integridad de balances
- consistencia de agregaciones
- coherencia entre Gold y resultados SQL

### Documentación

#### Repositorio SQL

Organizar:

- scripts SQL
- consultas reutilizables
- documentación de métricas

### Resultado esperado

Primer entorno SQL funcional orientado a análisis financiero y consumo analítico.

---

## Semana 17–18 — SQL Analítico Financiero (Parte 2)

### Objetivo real

Profundizar el análisis financiero mediante SQL intermedio y comenzar la construcción de métricas reutilizables para Business Intelligence.

### SQL intermedio

#### Consultas avanzadas

Implementar:

- CTEs
- subqueries
- CASE WHEN
- funciones agregadas avanzadas
- validaciones cruzadas

### SQL avanzado

#### Análisis temporal

Implementar:

- acumulados
- comparativos mensuales
- tendencias
- análisis por períodos

#### Window Functions

Explorar:

- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- SUM() OVER()
- AVG() OVER()

### Métricas financieras reutilizables

#### Indicadores analíticos

Construir:

- tendencias de movimientos
- evolución mensual
- comportamiento de cuentas
- análisis comparativos

### Calidad analítica

#### Validaciones

Verificar:

- consistencia de métricas
- integridad de agregaciones
- calidad de resultados

### Resultado esperado

Modelo SQL más robusto y preparado para alimentar futuros dashboards financieros.

---

## Semana 19–20 — Construcción de KPIs Financieros y Operativos

### Objetivo real

Transformar datasets Gold y consultas SQL en indicadores reutilizables para análisis financiero y operacional.

### KPIs financieros

#### Accounting

Construir indicadores como:

- crecimiento mensual
- variaciones financieras
- comportamiento por cuenta
- distribución de movimientos
- tendencias financieras

### KPIs operativos

#### Inventory

Construir indicadores como:

- movimientos por producto
- rotación básica
- referencias más utilizadas
- comportamiento de inventario

#### Manufacturing

Construir indicadores como:

- órdenes procesadas
- estados operativos
- cantidades producidas
- actividad operacional

### Estandarización

#### Catálogo de KPIs

Documentar:

- definición
- fórmula
- origen de datos
- frecuencia de actualización

### Validaciones

#### Consistencia de indicadores

Verificar:

- integridad de cálculos
- consistencia entre SQL y Gold
- calidad de métricas

### Resultado esperado

KPIs financieros y operativos listos para consumo analítico y Business Intelligence.

---

## Semana 21–22 — Construcción Inicial de Dashboards en Power BI

### Objetivo real

Conectar datasets Gold y KPIs a Power BI para construir las primeras visualizaciones analíticas del proyecto.

### Prioridad principal

#### Conexión de datos

Integrar:

- financial_summary
- inventory_summary
- production_summary
- KPIs construidos previamente

### Dashboard financiero

#### Finanzas

Implementar visualizaciones para:

- balances
- movimientos financieros
- tendencias
- variaciones mensuales
- KPIs financieros

### Dashboard operativo

#### Inventario

Implementar visualizaciones para:

- entradas y salidas
- movimientos de productos
- comportamiento operativo

#### Producción

Implementar visualizaciones para:

- órdenes
- estados operativos
- actividad de manufactura

### Modelado básico

#### Power BI

Implementar:

- relaciones básicas
- medidas iniciales
- segmentadores
- filtros

### Resultado esperado

Primer entorno BI funcional conectado directamente a los datasets analíticos del proyecto.

---

## Semana 23–24 — Consolidación Analítica y Validación BI

### Objetivo real

Validar la consistencia entre datasets Gold, consultas SQL, KPIs y dashboards para garantizar información confiable y útil para análisis financiero y operativo.

### Prioridad principal

#### Validación de métricas

Verificar:

- consistencia de KPIs
- integridad de agregaciones
- coherencia entre SQL y Power BI
- estabilidad de cálculos

### Calidad analítica

#### Validaciones funcionales

Revisar:

- filtros
- segmentadores
- medidas
- relaciones
- tablas de soporte

#### Consistencia de resultados

Comparar:

- resultados SQL
- datasets Gold
- visualizaciones Power BI
- métricas calculadas

### Optimización analítica

#### Mejoras de usabilidad

Implementar:

- nombres más descriptivos
- organización visual
- navegación más intuitiva
- documentación básica de dashboards

### Validación financiera

#### Dominio Accounting

Confirmar:

- balances consistentes
- métricas correctas
- movimientos consolidados
- trazabilidad de cifras

### Resultado esperado

Entorno BI estable, consistente y preparado para presentación profesional.

---

## Semana 25–26 — Consolidación Arquitectónica y Optimización

### Objetivo real

Reducir redundancia, mejorar mantenibilidad y estabilizar completamente la arquitectura reusable del proyecto.

### Prioridad principal

#### Refactorización general

Revisar:

- módulos existentes
- funciones duplicadas
- lógica repetida
- dependencias innecesarias

### Optimización técnica

#### Pipeline ETL

Mejorar:

- rendimiento de transformaciones
- eficiencia de validaciones
- reutilización de componentes
- trazabilidad del flujo

### Consolidación de código

#### Centralización

Fortalecer:

- generic_validations.py
- business_rules.py
- cleaning.py
- utilidades compartidas

#### Organización del proyecto

Asegurar:

- separación de responsabilidades
- consistencia de estructura
- facilidad de mantenimiento

### Calidad técnica

#### Testing

Ampliar:

- cobertura de pruebas
- escenarios de integración
- pruebas sobre datasets completos

### Resultado esperado

Pipeline financiero robusto, mantenible y preparado para crecimiento futuro.

---

## Semana 27–28 — Storytelling Técnico y Profesionalización del Proyecto

### Objetivo real

Convertir el proyecto completo en un caso de estudio sólido para Financial Data Analytics, Business Intelligence y analítica financiera.

### Documentación profesional

#### README avanzado

Documentar:

- arquitectura Medallion
- flujo ETL
- validaciones financieras
- Silver Layer
- Gold Layer
- SQL analítico
- Power BI

### Storytelling del proyecto

#### Evolución profesional

Explicar:

- punto de partida
- problemas encontrados
- decisiones tomadas
- aprendizajes obtenidos
- evolución técnica del proyecto

### Caso de negocio

#### Valor analítico

Destacar:

- calidad del dato
- confiabilidad de información financiera
- reducción de reprocesos
- preparación para análisis y reporting

### Portafolio profesional

#### Material visual

Preparar:

- capturas de código
- capturas de pruebas automatizadas
- capturas de Power BI
- diagramas de arquitectura
- diagramas del flujo ETL

### Preparación para entrevistas

#### Narrativa profesional

Construir explicación clara sobre:

- arquitectura implementada
- validaciones desarrolladas
- decisiones técnicas
- impacto analítico
- aplicación al contexto financiero

### Optimización de presencia profesional

#### GitHub y LinkedIn

Actualizar:

- README final
- documentación del proyecto
- publicaciones de seguimiento
- evidencias de avance
- descripción profesional del proyecto

### Resultado esperado

Proyecto completamente documentado, explicable, demostrable y listo para utilizarse como pieza principal de portafolio para posiciones de:

- Financial Data Analyst
- Financial BI Analyst
- Business Intelligence Analyst
- Data Analyst enfocado en finanzas
- Reporting & Insights Analyst