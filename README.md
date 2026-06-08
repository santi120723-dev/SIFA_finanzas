# SIFA_finanzas-Pipeline_ETL_para_Finanzas_(Python+Pandas)

## Resumen Ejecutivo

Este proyecto implementa un pipeline ETL modular orientado a datos financieros reales utilizando Python y Pandas. El sistema procesa libros mayores heterogéneos mediante una arquitectura Medallion (Bronze → Silver → Gold), incorporando validaciones contables, limpieza reusable, logging centralizado, pruebas automatizadas, control de calidad de datos y trazabilidad de validaciones.

Durante las primeras etapas del proyecto se construyó una base robusta para la preparación y validación de información financiera, integrando reglas de negocio contables, validaciones estructurales, validaciones de calidad del dato y pruebas automatizadas sobre datasets reales.

Actualmente el proyecto cuenta con un flujo funcional:

Bronze → Load → Clean → Validate → Export Silver

preparado para soportar futuras capas analíticas, SQL financiero y Business Intelligence.

---

## Descripción

Proyecto enfocado en transformar datasets contables inconsistentes en información estructurada, validada y reutilizable para futuros procesos analíticos y dashboards financieros.

Actualmente incluye:

### Pipeline ETL modular

Separación clara entre:

* ingestión
* limpieza
* validación
* exportación Silver
* preparación analítica

### Arquitectura Medallion

Organización de datasets en:

* Bronze
* Silver
* Gold (preparación inicial)

### Validaciones financieras y de calidad

Implementación de validaciones críticas y advertencias para detectar:

* errores estructurales
* inconsistencias contables
* tipos de datos incorrectos
* valores fuera de rango
* registros duplicados
* datasets vacíos

### Limpieza reusable

Funciones desacopladas para:

* normalización de columnas
* manejo de nulos
* limpieza de strings
* enriquecimiento financiero
* preparación de datasets reutilizables

### Testing automatizado

Cobertura mediante pytest para:

* ingestión
* limpieza financiera
* validaciones contables
* validaciones genéricas
* validaciones de calidad
* validaciones de jerarquía contable
* integración del pipeline
* observabilidad de validaciones

---

## Estado del Proyecto

### Implementado (Funcional)

#### Arquitectura Medallion

* Directorios definidos:

  * data/bronze/
  * data/silver/
  * data/gold/

* Separación por dominios:

  * accounting/
  * inventory/
  * manufacturing/

* Configuración centralizada mediante `src/config.py`

* Uso de `pathlib.Path` para manejo robusto de rutas

---

#### Capa Bronze (Ingestion)

##### Funcionalidades implementadas

Archivo:

`src/ingestion/extract.py`

Implementado:

* `load_file()`
* `load_libro_mayor()`
* `load_movimientos_inventario()`
* `load_ordenes_fabricacion()`

##### Validaciones iniciales

* archivo existente
* formato soportado
* DataFrame no vacío
* logging automático de errores

##### Testing

* carga correcta de CSV
* carga correcta de Excel
* archivo inexistente
* formato inválido

---

#### Capa Silver (Transformación y Limpieza)

##### Limpieza reusable

Archivo:

`src/utils/cleaning.py`

Funciones implementadas:

* normalize_column_names()
* clean_strings()
* handle_nulls()
* clean_dataframe()

##### Transformaciones financieras

Archivo:

`src/transformations/accounting_cleaning.py`

Implementado:

* detección automática de cuentas
* forward fill de cuentas contables
* detección de balances iniciales
* corrección de fechas
* eliminación de filas de totales
* eliminación de cabeceras intermedias
* cálculo de valor_movimiento
* construcción de jerarquía PUC
* construcción de calendario financiero

---

#### Enriquecimiento Financiero

Implementado:

* valor_movimiento = debe - haber

Objetivo:

* facilitar análisis financieros posteriores
* preparar indicadores financieros
* soportar reportería financiera

---

#### Jerarquía Contable PUC

Implementado:

* clase
* grupo
* cuenta_puc
* subcuenta

Objetivo:

* soportar agregaciones financieras
* facilitar análisis por niveles contables
* preparar datasets analíticos

---

#### Calendario Financiero

Implementado:

* anio
* mes
* trimestre
* periodo_contable

Objetivo:

* análisis temporal
* reportería financiera
* Business Intelligence

---

#### Exportación Silver

Archivo:

`src/utils/export_silver.py`

Implementado:

* exportación Parquet
* creación automática de directorios
* persistencia en Silver Layer
* trazabilidad mediante logging

Resultado:

* generación automática de datasets listos para análisis

---

#### Pipeline ETL Integrado

Archivo:

`src/orchestration/run_pipeline.py`

Flujo implementado:

Bronze

↓

Load

↓

Clean

↓

Validate

↓

Export Silver

Funcionalidades:

* integración de módulos ETL
* ejecución desacoplada
* validaciones automáticas
* exportación automática a Silver
* trazabilidad de ejecución

Resultado:

* pipeline reutilizable para datasets financieros

---

#### Sistema de Validaciones

Carpeta:

`src/validations/`

##### Componentes implementados

* severity.py
* generic_validations.py
* business_rules.py
* accounting_validations.py
* warning_validations.py
* data_type_validations.py
* value_range_validations.py
* account_hierarchy_validations.py
* validation_summary.py
* validation_runner.py

---

#### Severidades implementadas

Actualmente el pipeline diferencia formalmente entre:

##### CRITICAL

Errores que deben detener la ejecución del pipeline.

##### WARNING

Situaciones que no detienen la ejecución pero requieren monitoreo y seguimiento.

Implementado mediante:

* severity.py
* validation_runner.py

Objetivo:

* mejorar control operativo
* separar errores críticos de alertas de calidad
* facilitar monitoreo de datos financieros

---

#### Validaciones Críticas

Actualmente el pipeline ejecuta:

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

Objetivo:

* garantizar integridad financiera
* detectar errores estructurales
* prevenir inconsistencias antes de exportar a Silver

---

#### Validaciones WARNING

Actualmente el pipeline ejecuta:

* validate_nulls()
* validate_empty_dataframe()
* validate_duplicates()

Objetivo:

* monitorear calidad del dato
* detectar posibles anomalías
* mejorar trazabilidad y seguimiento

---

#### Validación de Jerarquía Contable

Archivo:

`src/validations/account_hierarchy_validations.py`

Implementado:

* validate_account_hierarchy_consistency()

Validaciones incluidas:

* coherencia entre clase y código de cuenta
* coherencia entre grupo y clase
* coherencia entre cuenta_puc y grupo
* coherencia entre subcuenta y cuenta_puc

Objetivo:

* detectar inconsistencias estructurales dentro de la jerarquía PUC
* proteger reportería financiera
* mejorar consistencia contable

---

#### Validation Runner

Implementado mediante:

`run_validations()`

Funcionalidades:

* ejecución centralizada
* clasificación por severidad
* retorno estructurado de resultados
* integración con logging
* integración con pipeline ETL

Resultado:

* validaciones reutilizables y desacopladas

---

#### Resumen Consolidado de Validaciones

Archivo:

`src/validations/validation_summary.py`

Implementado:

* generación de resumen consolidado
* conteo por severidad
* consolidación de errores
* consolidación de advertencias

Objetivo:

* mejorar observabilidad
* mejorar monitoreo
* facilitar análisis de calidad del dato

Resultado:

* mayor trazabilidad de la ejecución de validaciones

---

#### Calidad del Dato y Observabilidad

Actualmente la Silver Layer incorpora controles para:

* integridad contable
* consistencia estructural
* calidad de datos
* trazabilidad de validaciones
* monitoreo de advertencias
* prevención de errores silenciosos

Beneficios:

* reducción de riesgos en reportería financiera
* mayor confiabilidad analítica
* mejor preparación para Business Intelligence

---

#### Logging y Trazabilidad

Archivo:

`src/logger.py`

Implementado:

* logging centralizado
* salida en consola
* generación de logs persistentes
* registro de errores
* registro de warnings
* trazabilidad de validaciones
* seguimiento de ejecución del pipeline

Archivo de salida:

`logs/pipeline.log`

Objetivo:

* facilitar debugging
* mejorar monitoreo operativo
* fortalecer trazabilidad de ejecución

---

#### Testing Automatizado

Carpeta:

`tests/`

Cobertura actual:

##### Ingestión

* carga CSV
* carga Excel
* formatos inválidos
* archivos inexistentes

##### Limpieza financiera

* forward fill
* balances iniciales
* eliminación de totales
* jerarquía PUC
* calendario financiero

##### Validaciones contables

* código de cuenta
* nombre de cuenta
* fecha
* estructura PUC
* valor_movimiento
* debe/haber

##### Calidad de datos

* tipos de datos
* rangos permitidos
* nulos
* duplicados
* datasets vacíos

##### Jerarquía contable

* consistencia de clase
* consistencia de grupo
* consistencia de cuenta_puc
* consistencia de subcuenta

##### Observabilidad

* resumen consolidado de validaciones

##### Integración

* pipeline completo Bronze → Silver

Resultado actual:

* 50 pruebas automatizadas
* 50 pruebas aprobadas

---

#### Datasets de Prueba

Actualmente existen datasets de soporte para testing:

* bronze_test.csv
* bronze_test.xlsx
* critical_imbalanced.csv
* critical_imbalanced2.csv
* invalid_dates.csv
* null_dates.csv
* duplicates.csv
* no_duplicates.csv
* missing_columns.csv

Objetivo:

* reproducibilidad de pruebas
* validación consistente del pipeline
* simulación de escenarios reales

---

### Estado Actual de la Silver Layer

La Silver Layer financiera cuenta actualmente con:

* pipeline ETL integrado
* limpieza reusable
* enriquecimiento financiero
* jerarquía contable PUC
* calendario financiero
* validaciones críticas
* validaciones warning
* control de severidades
* validación de jerarquía contable
* resumen consolidado de validaciones
* exportación automática a Parquet
* logging centralizado
* pruebas automatizadas
* pruebas de integración end-to-end

Flujo actual:

Bronze

↓

Load

↓

Clean

↓

Validate

↓

Export Silver

La capa Silver se encuentra consolidada y preparada para servir como base de futuros procesos analíticos, modelado de datos, SQL financiero y Business Intelligence.

---

### Tecnologías Utilizadas

#### Core

* Python 3.11.7
* Pandas
* Pathlib

#### Calidad y Testing

* Pytest
* Validaciones CRITICAL/WARNING
* Testing de integración
* Testing de reglas contables
* Testing de calidad del dato

#### Herramientas

* Git
* GitHub
* VS Code
* Jupyter Notebook
* Logging estándar de Python

---

### Lecciones Aprendidas

* La calidad del dato debe validarse antes de cualquier proceso analítico.
* Las reglas contables requieren respaldo mediante pruebas automatizadas para garantizar confiabilidad.
* La separación entre validaciones críticas y advertencias mejora el control operativo del pipeline.
* La observabilidad y trazabilidad son tan importantes como las transformaciones de datos.
* La integración temprana de testing reduce significativamente el riesgo de errores silenciosos.
* Una Silver Layer sólida simplifica la construcción posterior de modelos analíticos y dashboards financieros.

---

### Próximos Pasos

#### Semana 7 — Gobierno de Datos y Dimensión de Terceros

Implementar:

* extracción de terceros desde la base de datos
* construcción de dimensión de terceros
* anonimización de información sensible
* generación de identificadores trazables

Ejemplo:

* TERCERO_000001
* TERCERO_000002
* TERCERO_000003

También se incorporará:

* tabla de mapeo controlada
* integración con la Silver Layer
* trazabilidad entre identificador anonimizado y tercero original

Objetivo:

Preparar el proyecto para análisis financieros por terceros manteniendo principios de trazabilidad, gobierno de datos y protección de información sensible.

---

### Caso de Uso

Simulación de un pipeline financiero orientado a Business Intelligence, calidad del dato y analítica financiera sobre datasets reales.

El proyecto busca representar escenarios comunes de integración ETL financiera, control de calidad, validaciones contables, gobierno de datos y preparación analítica para reportería financiera, análisis de negocio y futuras soluciones de Business Intelligence.