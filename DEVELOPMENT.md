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

#### Sistema base de validaciones consolidado

Ya implementaste correctamente la estructura principal de validaciones:

* src/validations/severity.py
* src/validations/generic_validations.py
* src/validations/business_rules.py
* src/validations/validation_runner.py
* src/validations/warning_validations.py
* src/validations/accounting_validations.py

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
* validate_codigo_cuenta()
* validate_nombre_cuenta()
* validate_fecha_datetime()
* validate_puc_structure()
* validate_valor_movimiento()

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
* validaciones contables
* estructura PUC
* valor_movimiento
* validación de fechas datetime

Resultado actual:

* 17 pruebas automatizadas
* 17 pruebas aprobadas

✔ Las validaciones principales cuentan con cobertura automatizada.

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

### Resultado de la semana

Se consolidó un framework de validaciones reutilizable, desacoplado y preparado para soportar múltiples dominios de negocio, permitiendo controlar calidad de datos y consistencia financiera dentro del pipeline ETL.

---

## Semana 6 — Integración del Pipeline y Consolidación de Silver Layer

### Objetivo

Construir el primer flujo ETL reutilizable completo:

Bronze → Clean → Validate → Silver

dejando una Silver Layer financiera estable, validada y preparada para futuras transformaciones analíticas.

---

#### Integración formal del pipeline

Se consolidó exitosamente:

* load_libro_mayor()
* clean_dataframe()
* run_validations()
* export_silver()
* run_pipeline()

mediante:

* src/orchestration/run_pipeline.py

✔ El flujo ETL completo quedó integrado y funcional.

---

#### Pipeline Silver operativo

Actualmente el flujo ejecuta:

Bronze

↓

Load

↓

Clean

↓

Validate

↓

Export Silver

✔ El pipeline procesa correctamente datasets financieros reales y genera automáticamente la salida en Silver Layer.

---

#### Exportación Silver implementada

Se implementó:

* export_silver()
* exportación Parquet
* creación automática de rutas
* persistencia en data/silver/accounting
* trazabilidad de archivos exportados

✔ La Silver Layer financiera quedó operativa.

---

#### Transformaciones contables implementadas

Se construyeron reglas específicas para Libro Mayor:

* detección automática de cabeceras
* propagación de cuentas mediante forward fill
* asignación de codigo_cuenta
* asignación de nombre_cuenta
* detección de balances iniciales
* corrección de fechas de balance inicial
* eliminación de filas Total
* eliminación de cabeceras intermedias
* generación de detalle_movimiento

✔ La estructura contable queda correctamente propagada a todos los movimientos.

---

#### Enriquecimiento financiero implementado

Se incorporó:

* valor_movimiento = debe - haber

✔ El dataset quedó preparado para análisis financieros posteriores.

---

#### Jerarquía contable PUC implementada

Se construyeron:

* clase
* grupo
* cuenta_puc
* subcuenta

✔ El dataset quedó preparado para agregaciones financieras y análisis jerárquicos.

---

#### Calendario financiero implementado

Se construyeron:

* anio
* mes
* trimestre
* periodo_contable

✔ El dataset quedó preparado para análisis temporal y Business Intelligence.

---

#### Validaciones financieras integradas

Actualmente el pipeline valida automáticamente:

##### Validaciones CRITICAL

* validate_required_columns()
* validate_dates()
* validate_debe_haber()
* validate_codigo_cuenta()
* validate_nombre_cuenta()
* validate_fecha_datetime()
* validate_puc_structure()
* validate_valor_movimiento()
* validate_data_types()
* validate_value_ranges()
* validate_account_hierarchy_consistency()

##### Validaciones WARNING

* validate_nulls()
* validate_empty_dataframe()
* validate_duplicates()

✔ La calidad financiera, estructural y jerárquica es verificada antes de exportar a Silver.

---

#### Sistema de severidades implementado

Actualmente existe una separación formal entre:

* CRITICAL
* WARNING

mediante:

* src/validations/severity.py
* src/validations/validation_runner.py

✔ El pipeline puede diferenciar errores que deben detener la ejecución de alertas de calidad que requieren seguimiento.

---

#### Observabilidad y trazabilidad de validaciones

Se implementó:

* validation_summary.py

Permitiendo consolidar:

* validaciones ejecutadas
* severidades detectadas
* resultados obtenidos
* advertencias registradas

✔ El pipeline cuenta con mayor observabilidad y seguimiento sobre la calidad del dato.

---

#### Test de integración implementado

Se implementó:

* test_pipeline_integration.py

Validando:

* carga correcta
* limpieza correcta
* ejecución de validaciones
* generación correcta de archivos Silver

✔ El flujo completo Bronze → Silver cuenta con validación automatizada end-to-end.

---

#### Testing automatizado implementado

Actualmente existen pruebas para:

##### Ingestión

* carga de archivos CSV
* carga de archivos Excel
* archivos inexistentes
* formatos inválidos

##### Cleaning

* forward fill de cuentas
* balance inicial
* eliminación de totales
* jerarquía PUC
* calendario financiero

##### Validaciones contables

* validate_codigo_cuenta()
* validate_nombre_cuenta()
* validate_fecha_datetime()
* validate_puc_structure()
* validate_valor_movimiento()
* validate_debe_haber()

##### Calidad de datos

* validate_data_types()
* validate_value_ranges()
* validate_nulls()
* validate_empty_dataframe()
* validate_duplicates()

##### Consistencia jerárquica

* validate_account_hierarchy_consistency()

Validando:

* clase ↔ código de cuenta
* grupo ↔ clase
* cuenta_puc ↔ grupo
* subcuenta ↔ cuenta_puc

##### Observabilidad

* test_validation_summary.py

##### Integración

* test_pipeline_integration.py

Resultado actual:

* 50 pruebas automatizadas
* 50 pruebas aprobadas

✔ La lógica crítica de Silver cuenta con cobertura automatizada, validaciones jerárquicas, observabilidad y pruebas de integración.

---

#### Datasets de prueba implementados

Actualmente existen datasets de soporte para testing como:

* bronze_test.csv
* bronze_test.xlsx
* critical_imbalanced.csv
* critical_imbalanced2.csv
* invalid_dates.csv
* null_dates.csv
* duplicates.csv
* no_duplicates.csv
* missing_columns.csv

✔ El comportamiento de las validaciones puede verificarse de forma reproducible.

---

### Resultado esperado

Silver Layer financiera completamente consolidada, validada, automatizada y respaldada mediante pruebas de integración, validaciones contables, controles de calidad de datos y observabilidad del pipeline.

Durante esta etapa se logró:

* Integración completa del flujo Bronze → Clean → Validate → Silver.
* Implementación de transformaciones contables reutilizables para Libro Mayor.
* Construcción de jerarquía contable PUC y calendario financiero.
* Incorporación de validaciones financieras, estructurales y de calidad de datos.
* Separación formal entre validaciones CRITICAL y WARNING.
* Implementación de validaciones de consistencia jerárquica contable.
* Incorporación de observabilidad mediante resúmenes consolidados de validaciones.
* Ejecución exitosa de pruebas unitarias, funcionales y de integración.

Resultado final:

* 50 pruebas automatizadas.
* 50 pruebas aprobadas.

✔ La Silver Layer financiera queda consolidada como una base confiable para soportar futuras etapas de análisis financiero, reportería, Business Intelligence y construcción de la capa Gold.

---

## Semana 7 — Gobierno de Datos y Preparación de la Gold Layer

### Objetivo

Enriquecer la información financiera validada de la Silver Layer incorporando la gestión de terceros, anonimización de datos sensibles y preparación de datasets orientados a análisis financiero, reportería y Business Intelligence.

---

#### Incorporación de terceros al modelo financiero

Extraer desde la base de datos corporativa la información necesaria para complementar el Libro Mayor con:

* documento
* tipo_documento
* nombre_tercero

cuando la información se encuentre disponible.

El objetivo es fortalecer la identificación de entidades financieras dentro del modelo de datos.

✔ La información financiera contará con una referencia única para cada tercero.

---

#### Construcción de dimensión de terceros

Implementar una estructura centralizada para terceros financieros:

##### dim_terceros

Incluyendo:

* documento
* tipo_documento
* nombre_tercero
* identificador interno

Esta dimensión permitirá:

* consolidación por tercero
* análisis de concentración
* reportería por cliente o proveedor
* futuras relaciones analíticas en Gold Layer

✔ Se establece una entidad maestra para análisis financieros posteriores.

---

#### Sistema de anonimización de información sensible

Implementar una estrategia de anonimización para proteger información corporativa y personal.

Transformando:

* nombres reales
* terceros
* contactos
* documentos

en identificadores controlados:

* TERCERO_000001
* TERCERO_000002
* TERCERO_000003

manteniendo la consistencia entre registros relacionados.

✔ Los datasets podrán utilizarse en pruebas, GitHub, portafolio y dashboards sin exponer información real.

---

#### Tabla de trazabilidad de anonimización

Construir una tabla de correspondencia controlada:

##### terceros_mapping

Ejemplo:

| tercero_id     | documento | nombre_real |
| -------------- | --------- | ----------- |
| TERCERO_000001 | 900123456 | Empresa A   |
| TERCERO_000002 | 800999888 | Empresa B   |

Esta tabla:

* permanecerá separada del dataset analítico
* no será utilizada en publicaciones
* permitirá auditoría y trazabilidad interna

✔ Se conserva la capacidad de reconciliación sin comprometer privacidad.

---

#### Calidad de datos para terceros

Incorporar validaciones orientadas a:

* terceros duplicados
* documentos faltantes
* inconsistencias entre documento y nombre
* registros huérfanos
* problemas de identificación

✔ Se fortalece la calidad de la dimensión de terceros antes de procesos analíticos.

---

#### Construcción de datasets analíticos

Preparar datasets derivados desde Silver para facilitar:

* análisis financiero
* reportería ejecutiva
* indicadores financieros
* futuras visualizaciones BI

Se evaluará la construcción de datasets orientados a:

* movimientos por cuenta
* movimientos por tercero
* análisis temporal
* consolidación financiera

✔ La información comenzará a estructurarse para consumo analítico.

---

#### Diseño inicial de Gold Layer

Definir la estructura inicial para:

* data/gold/finance
* data/gold/management
* data/gold/operations

Estableciendo:

* dimensiones
* métricas
* granularidad
* criterios de agregación

✔ Se preparan las bases para la futura capa Gold.

---

#### Testing automatizado

Implementar pruebas para:

* generación de terceros anonimizados
* consistencia de identificadores
* integridad de tablas de mapeo
* calidad de la dimensión de terceros
* generación de datasets analíticos

✔ Los nuevos procesos quedarán respaldados mediante pruebas automatizadas.

---

### Resultado esperado

La plataforma evolucionará desde una Silver Layer validada hacia una arquitectura preparada para análisis financiero y Business Intelligence mediante:

* gestión estructurada de terceros
* anonimización de información sensible
* trazabilidad controlada
* datasets analíticos reutilizables
* preparación formal de la Gold Layer

La información financiera quedará lista para soportar futuros KPIs, reportería ejecutiva, SQL analítico y dashboards de Business Intelligence.

---

## Semana 8 — Construcción Inicial de Gold Layer Financiera

### Objetivo

Construir los primeros datasets analíticos derivados de la Silver Layer financiera, preparando la información para reportería financiera, KPIs y Business Intelligence.

---

### Prioridad Principal

#### Diseño de Gold Layer

Crear:

* data/gold/
* estructura de datasets analíticos
* reglas de agregación
* organización por dominios analíticos

---

### Modelo analítico inicial

Diseñar una primera estructura dimensional compuesta por:

#### Dimensiones

* dim_calendario
* dim_cuentas
* dim_terceros

#### Hechos

* fact_movimientos_financieros

✔ Se establece una base preparada para análisis y BI.

---

### Primer dataset Gold

#### financial_summary

Construir agregaciones por:

* periodo_contable
* clase
* grupo
* cuenta_puc
* subcuenta

---

### Dataset analítico por terceros

#### financial_summary_by_third_party

Construir agregaciones por:

* tercero_id
* periodo_contable
* clase
* grupo

Incorporando la anonimización implementada en Semana 7.

✔ Se habilita el análisis financiero por terceros sin exponer información sensible.

---

### Métricas iniciales

Generar:

* total_debe
* total_haber
* total_movimientos
* valor_neto
* cantidad_movimientos

---

### Exportación Gold

Implementar:

* export_gold()
* exportación Parquet
* control de versiones
* organización de datasets analíticos

---

### Validaciones Gold

Verificar:

* consistencia Silver vs Gold
* integridad de agregaciones
* ausencia de pérdidas de registros
* consistencia de dimensiones
* correcta anonimización de terceros

---

### Preparación para BI

Generar datasets optimizados para:

* Power BI
* reportería financiera
* indicadores financieros
* análisis temporal
* análisis por terceros

---

### Resultado esperado

Primer ecosistema Gold financiero compuesto por datasets analíticos reutilizables, dimensiones financieras y estructuras preparadas para Business Intelligence, reportería financiera y construcción de KPIs.

---

## Semana 9 — KPIs Financieros y Primer Dashboard de Business Intelligence

### Objetivo

Transformar los datasets Gold en información de negocio mediante indicadores financieros y visualizaciones analíticas.

---

#### Definición de KPIs

Construir indicadores como:

* ingresos por periodo
* gastos por periodo
* resultado neto
* variación mensual
* participación por grupo de cuentas
* concentración por terceros

---

#### Modelo para Power BI

Preparar:

* relaciones
* medidas
* tablas de hechos
* dimensiones

✔ Modelo listo para consumo analítico.

---

#### Dashboard financiero inicial

Visualizar:

* evolución temporal
* ingresos vs gastos
* análisis por cuentas
* análisis por terceros
* indicadores ejecutivos

---

#### Validación de indicadores

Verificar:

* consistencia con Gold Layer
* integridad de métricas
* trazabilidad de cálculos

---

### Resultado esperado

Primer dashboard financiero funcional construido sobre una arquitectura Medallion completa:

Bronze → Silver → Gold → BI

## Semana 10 — Consolidación de Gobierno de Datos

### Objetivo

Formalizar la gestión de terceros y documentar las reglas de anonimización y trazabilidad implementadas.

#### Diccionario de terceros

Documentar:

* tercero_id
* documento
* tipo_documento
* nombre_tercero

✔ Se mejora la comprensión del modelo de datos.

---

#### Reglas de anonimización

Documentar:

* generación de identificadores
* consistencia de mapeos
* reutilización de identificadores

✔ Se fortalece la gobernanza de datos.

---

#### Pruebas automatizadas

Incorporar:

* pruebas de consistencia de terceros
* pruebas de trazabilidad
* pruebas de anonimización

✔ La gestión de terceros queda respaldada por evidencia automatizada.

---

### Resultado esperado

Gobierno de datos implementado y documentado para soportar futuras capas analíticas.

## Semana 11 — Diseño Dimensional de Gold Layer

### Objetivo

Diseñar la primera estructura dimensional financiera para soportar reportería y Business Intelligence.

#### Dimensión de cuentas

Construir:

* dim_cuentas

Incluyendo:

* clase
* grupo
* cuenta_puc
* subcuenta
* nombre_cuenta

✔ Se centraliza la estructura contable.

---

#### Dimensión calendario

Construir:

* dim_calendario

Incluyendo:

* fecha
* anio
* mes
* trimestre
* periodo_contable

✔ Se habilita análisis temporal estandarizado.

---

#### Dimensión terceros

Construir:

* dim_terceros

Basada en:

* tercero_id
* tipo_documento

✔ Se prepara el análisis financiero por tercero.

---

### Resultado esperado

Modelo dimensional inicial definido para la futura Gold Layer.

## Semana 12 — Construcción de la Tabla de Hechos Financiera

### Objetivo

Construir la primera tabla de hechos financiera que servirá como base para reportería, KPIs y Business Intelligence.

#### Fact Table Financiera

Construir:

* fact_movimientos_financieros

Incluyendo:

* fecha
* tercero_id
* codigo_cuenta
* debe
* haber
* valor_movimiento
* periodo_contable

✔ Se consolida una fuente única para análisis financiero.

---

#### Integración de dimensiones

Relacionar:

* dim_calendario
* dim_cuentas
* dim_terceros

✔ Se establece la estructura dimensional inicial.

---

#### Validaciones de integridad

Verificar:

* claves válidas
* ausencia de registros huérfanos
* consistencia entre dimensiones y hechos

✔ Se garantiza calidad estructural para análisis.

---

### Resultado esperado

Primera tabla de hechos financiera lista para alimentar datasets Gold.

## Semana 13 — Construcción de Financial Summary

### Objetivo

Construir el primer dataset agregado para reportería financiera.

#### Dataset Financial Summary

Construir:

* financial_summary

Agrupando por:

* periodo_contable
* clase
* grupo
* cuenta_puc
* subcuenta

✔ Se obtiene una vista consolidada de movimientos financieros.

---

#### Métricas financieras

Generar:

* total_debe
* total_haber
* valor_neto
* cantidad_movimientos

✔ Se habilitan análisis financieros de alto nivel.

---

#### Exportación Gold

Implementar:

* export_gold()

Con salida en:

* data/gold/finance

✔ Se inicia formalmente la Gold Layer.

---

### Resultado esperado

Primer dataset Gold financiero disponible para reportería y análisis.

## Semana 14 — Construcción de Financial Summary by Third Party

### Objetivo

Extender la Gold Layer para soportar análisis financieros por terceros.

#### Dataset por terceros

Construir:

* financial_summary_by_third_party

Agrupando por:

* tercero_id
* periodo_contable
* clase
* grupo

✔ Se habilita análisis financiero por entidad.

---

#### Métricas por tercero

Generar:

* total_debe
* total_haber
* valor_neto
* cantidad_movimientos

✔ Se facilita la identificación de concentraciones financieras.

---

#### Validaciones analíticas

Verificar:

* correcta anonimización
* integridad de agregaciones
* consistencia entre Silver y Gold

✔ Se protege la calidad del análisis.

---

### Resultado esperado

Dataset financiero por terceros preparado para BI y reportería.

## Semana 15 — Validaciones y Conciliación de Gold Layer

### Objetivo

Asegurar que la información agregada en Gold conserve la integridad financiera de la Silver Layer.

#### Conciliación Silver vs Gold

Verificar:

* total_debe
* total_haber
* valor_neto
* cantidad_movimientos

✔ Las agregaciones reflejan correctamente los datos originales.

---

#### Validaciones dimensionales

Comprobar:

* integridad de dimensiones
* claves válidas
* relaciones consistentes

✔ Se fortalece la confiabilidad del modelo analítico.

---

#### Testing automatizado

Implementar:

* pruebas de conciliación
* pruebas de agregación
* pruebas dimensionales

✔ La Gold Layer queda respaldada mediante evidencia automatizada.

---

### Resultado esperado

Gold Layer financiera validada y conciliada.

## Semana 16 — KPIs Financieros Básicos

### Objetivo

Transformar los datasets Gold en indicadores financieros reutilizables.

#### KPIs financieros iniciales

Construir:

* ingresos_totales
* gastos_totales
* resultado_neto

✔ Se generan métricas financieras fundamentales.

---

#### Métricas por periodo

Calcular:

* resultado_mensual
* resultado_trimestral
* resultado_anual

✔ Se habilita seguimiento financiero temporal.

---

#### Documentación de indicadores

Registrar:

* definición
* fórmula
* fuente de datos

✔ Se mejora trazabilidad y gobernanza de métricas.

---

### Resultado esperado

Primer conjunto de KPIs financieros disponible para análisis y reportería.

## Semana 17 — KPIs Temporales y Tendencias Financieras

### Objetivo

Construir indicadores orientados al análisis temporal de la información financiera.

#### Variaciones Financieras

Calcular:

* variación mensual
* variación trimestral
* variación anual

✔ Se facilita el análisis de evolución financiera.

---

#### Tendencias

Generar:

* tendencias de ingresos
* tendencias de gastos
* tendencias de resultado neto

✔ Se identifican patrones de comportamiento financiero.

---

#### Comparativos

Implementar:

* periodo actual vs periodo anterior
* análisis de crecimiento

✔ Se fortalece el análisis de desempeño financiero.

---

### Resultado esperado

KPIs temporales preparados para reportería financiera y análisis de tendencias.

## Semana 18 — KPIs por Terceros

### Objetivo

Construir indicadores financieros enfocados en terceros para soportar análisis de concentración y comportamiento.

#### Concentración Financiera

Calcular:

* participación por tercero
* concentración de movimientos
* concentración de valores

✔ Se identifican terceros con mayor impacto financiero.

---

#### Ranking de Terceros

Generar:

* Top 10 terceros por movimiento
* Top 10 terceros por valor neto
* Top 10 terceros por volumen de transacciones

✔ Se facilita la identificación de actores relevantes.

---

#### Indicadores de Participación

Construir:

* porcentaje de participación
* acumulados por tercero

✔ Se mejora la capacidad de análisis financiero.

---

### Resultado esperado

Conjunto de KPIs financieros orientados a terceros y análisis de concentración.

## Semana 19 — Catálogo de Métricas Financieras

### Objetivo

Documentar formalmente los indicadores construidos dentro de la Gold Layer.

#### Diccionario de KPIs

Documentar:

* nombre del KPI
* descripción
* fórmula
* fuente de datos
* periodicidad

✔ Se mejora la gobernanza de métricas.

---

#### Trazabilidad

Relacionar:

* KPI
* dataset origen
* dimensiones utilizadas

✔ Se facilita auditoría y mantenimiento.

---

#### Estandarización

Definir:

* convenciones de nombres
* estructura de métricas
* criterios de cálculo

✔ Se garantiza consistencia analítica.

---

### Resultado esperado

Catálogo financiero formalizado para reportería y Business Intelligence.

## Semana 20 — SQL Analítico Básico

### Objetivo

Incorporar SQL como herramienta de análisis sobre los datasets financieros generados.

#### Consultas Básicas

Construir:

* filtros
* agrupaciones
* ordenamientos
* joins

✔ Se fortalece la capacidad de análisis de datos.

---

#### Consultas Financieras

Implementar consultas para:

* movimientos por cuenta
* movimientos por periodo
* movimientos por tercero

✔ Se facilita la exploración financiera mediante SQL.

---

#### Organización

Crear:

* sql/gold/

para almacenar consultas reutilizables.

✔ Se establece una capa analítica SQL inicial.

---

### Resultado esperado

Primer conjunto de consultas financieras reutilizables.

## Semana 21 — SQL Financiero y Data Marts

### Objetivo

Construir consultas financieras avanzadas y preparar estructuras reutilizables para reportería.

#### Consultas Analíticas

Desarrollar:

* análisis temporal
* análisis por cuenta
* análisis por tercero
* análisis por jerarquía PUC

✔ Se amplía la capacidad de análisis financiero.

---

#### Data Marts

Construir:

* mart_financial_summary
* mart_third_party_analysis

✔ Se preparan datasets optimizados para consumo analítico.

---

#### Optimización

Evaluar:

* reutilización de consultas
* eficiencia de agregaciones
* simplificación de reportería

✔ Se fortalece la preparación para BI.

---

### Resultado esperado

Data marts financieros listos para alimentar dashboards y reportería.

## Semana 22 — Modelo Analítico para Power BI

### Objetivo

Preparar la Gold Layer para consumo eficiente desde herramientas de Business Intelligence.

#### Modelo Relacional

Construir relaciones entre:

* fact_movimientos_financieros
* dim_calendario
* dim_cuentas
* dim_terceros

✔ Se establece un modelo dimensional orientado a análisis.

---

#### Optimización Analítica

Validar:

* cardinalidades
* integridad referencial
* consistencia de relaciones

✔ Se garantiza estabilidad para reportería.

---

#### Preparación para BI

Definir:

* métricas base
* jerarquías
* dimensiones navegables

✔ El modelo queda preparado para Power BI.

---

### Resultado esperado

Modelo analítico financiero listo para consumo en herramientas BI.

## Semana 23 — Dashboard Financiero Operativo

### Objetivo

Construir el primer dashboard financiero utilizando la información consolidada en Gold Layer.

#### Visualizaciones

Implementar:

* ingresos por periodo
* gastos por periodo
* resultado neto
* evolución mensual

✔ Se obtiene visibilidad operativa de la información financiera.

---

#### Indicadores

Mostrar:

* ingresos acumulados
* gastos acumulados
* resultado acumulado

✔ Se facilita seguimiento financiero.

---

#### Validación

Verificar:

* consistencia contra Gold Layer
* exactitud de indicadores

✔ Se asegura confiabilidad de la reportería.

---

### Resultado esperado

Primer dashboard financiero operativo funcional.

## Semana 24 — Dashboard de Análisis por Terceros

### Objetivo

Construir visualizaciones orientadas al análisis financiero por terceros.

#### Indicadores

Implementar:

* top terceros por movimiento
* top terceros por valor neto
* concentración financiera

✔ Se identifican entidades con mayor impacto financiero.

---

#### Análisis Temporal

Visualizar:

* comportamiento histórico
* evolución por tercero

✔ Se facilita análisis de tendencias.

---

#### Protección de Datos

Utilizar:

* tercero_id anonimizado

✔ Se conserva privacidad sin afectar análisis.

---

### Resultado esperado

Dashboard especializado para análisis financiero por terceros.

## Semana 25 — Dashboard Ejecutivo Financiero

### Objetivo

Construir un dashboard orientado a toma de decisiones gerenciales.

#### KPIs Ejecutivos

Visualizar:

* ingresos
* gastos
* resultado neto
* crecimiento
* variaciones

✔ Se consolida información estratégica.

---

#### Resumen Financiero

Incorporar:

* comparativos mensuales
* comparativos trimestrales
* tendencias

✔ Se mejora capacidad de análisis gerencial.

---

#### Navegación

Implementar:

* filtros
* segmentaciones
* exploración por periodo

✔ Se facilita el análisis ejecutivo.

---

### Resultado esperado

Dashboard ejecutivo financiero listo para consumo gerencial.

## Semana 26 — Documentación Técnica Profesional

### Objetivo

Documentar formalmente la arquitectura y componentes de SIFA_FINANZAS.

#### Arquitectura

Documentar:

* Bronze Layer
* Silver Layer
* Gold Layer

✔ Se mejora mantenibilidad del proyecto.

---

#### Procesos ETL

Documentar:

* ingestión
* limpieza
* validaciones
* exportaciones

✔ Se facilita comprensión técnica.

---

#### Diagramas

Construir:

* flujo ETL
* arquitectura Medallion
* flujo de validaciones

✔ Se fortalece presentación profesional.

---

### Resultado esperado

Proyecto completamente documentado desde el punto de vista técnico.

## Semana 27 — Data Catalog y Diccionario de Datos

### Objetivo

Formalizar la documentación funcional y analítica de los datasets.

#### Diccionario de Datos

Documentar:

* columnas
* tipos de datos
* descripción funcional

✔ Se mejora gobernanza del dato.

---

#### Catálogo de Métricas

Documentar:

* KPIs
* fórmulas
* origen de datos

✔ Se fortalece trazabilidad analítica.

---

#### Catálogo de Validaciones

Documentar:

* validaciones críticas
* validaciones warning
* reglas contables

✔ Se consolida conocimiento funcional.

---

### Resultado esperado

Data Catalog completo para usuarios técnicos y de negocio.

## Semana 28 — Release 1.0 y Publicación Profesional

### Objetivo

Consolidar SIFA_FINANZAS como proyecto profesional de portafolio orientado a Analítica Financiera y Business Intelligence.

#### Revisión Integral

Validar:

* arquitectura
* datasets
* KPIs
* dashboards
* documentación

✔ Se garantiza consistencia global del proyecto.

---

#### Optimización Final

Revisar:

* rendimiento
* estructura
* organización del repositorio

✔ Se mejora calidad general del proyecto.

---

#### Portafolio

Preparar:

* README definitivo
* capturas de dashboards
* diagramas
* documentación técnica

✔ Se fortalece presentación profesional.

---

#### Publicación

Compartir:

* GitHub
* LinkedIn
* portafolio profesional

✔ El proyecto queda disponible como evidencia de competencias en:

* Python
* Pandas
* ETL
* Data Quality
* Data Governance
* SQL
* Business Intelligence
* Analítica Financiera

---

### Resultado esperado

Versión 1.0 de SIFA_FINANZAS finalizada y publicada como plataforma de Analítica Financiera construida de extremo a extremo.