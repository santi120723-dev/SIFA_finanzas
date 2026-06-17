# SIFA Finanzas

## Pipeline ETL Financiero con Gobierno de Datos, Calidad y Anonimización

---

# Resumen Ejecutivo

SIFA Finanzas es un proyecto de ingeniería y analítica de datos financieros que implementa un pipeline ETL modular para transformar información contable en datasets estructurados, validados y preparados para Business Intelligence.

El proyecto procesa información proveniente del Libro Mayor utilizando una arquitectura Medallion (Bronze → Silver → Gold), incorporando:

* limpieza y transformación de datos
* validaciones contables
* control de calidad
* trazabilidad de ejecución
* gobierno de datos
* gestión de terceros
* anonimización de información sensible
* pruebas automatizadas

Actualmente la plataforma permite procesar más de 250.000 movimientos contables, enriquecerlos con información de terceros, controlar la calidad del dato y generar datasets seguros para análisis, portafolio y Business Intelligence.

---

# Objetivo del Proyecto

Construir una plataforma de preparación y gobierno de datos financieros capaz de transformar información contable heterogénea en activos analíticos confiables para reportería financiera, análisis de negocio y futuras soluciones de Business Intelligence.

---

# Arquitectura

## Arquitectura Medallion

Bronze

↓

Silver

↓

Gold (en construcción)

### Bronze

Almacenamiento de datos fuente.

### Silver

Transformación, limpieza, validación, enriquecimiento y gobierno de datos.

### Gold

Modelos analíticos y métricas de negocio.

---

# Flujo Actual del Pipeline

Bronze

↓

Load

↓

Clean

↓

Financial Transformations

↓

Third Party Enrichment

↓

Data Validation

↓

Anonymization

↓

Dimension Building

↓

Export Silver

---

# Funcionalidades Implementadas

## Ingestión de Datos

Ubicación:

src/ingestion/

Capacidades:

* carga de archivos Excel
* carga de archivos CSV
* validación de formatos
* validación de existencia de archivos
* logging de errores

Datasets soportados:

* Libro Mayor
* Movimientos de Inventario
* Órdenes de Fabricación

---

## Limpieza y Estandarización

Ubicación:

src/utils/

Implementado:

* normalización de columnas
* limpieza de cadenas de texto
* manejo de valores nulos
* estandarización de formatos

---

## Transformaciones Financieras

Ubicación:

src/transformations/

Implementado:

* detección automática de cuentas
* forward fill contable
* eliminación de balances iniciales
* eliminación de cabeceras intermedias
* eliminación de totales
* cálculo de valor_movimiento
* generación de calendario financiero
* construcción de jerarquía PUC

Campos generados:

* valor_movimiento
* clase
* grupo
* cuenta_puc
* subcuenta
* anio
* mes
* trimestre
* periodo_contable

---

## Gobierno de Datos y Gestión de Terceros

Ubicación:

src/dimensions/

Implementado:

* construcción de maestro de terceros
* consolidación de clientes y proveedores
* matching automático
* detección de ambigüedades
* identificación de terceros no encontrados
* métricas de cobertura

Resultados obtenidos:

* 14.009 terceros evaluados
* 13.670 encontrados automáticamente
* 97 ambiguos
* 241 no encontrados
* cobertura de matching del 97,58%

Campos incorporados al Libro Mayor:

* documento
* tipo_tercero
* estado_matching

---

## Dimensión de Terceros

Implementada:

dim_terceros

Campos:

* tercero_id
* tipo_tercero
* estado_matching

Objetivos:

* análisis por tercero
* segmentación de clientes y proveedores
* reportería financiera
* reutilización analítica

---

## Anonimización de Datos

Ubicación:

src/privacy/

Implementado:

* generación de identificadores anónimos
* protección de información sensible
* datasets seguros para portafolio
* trazabilidad controlada

Ejemplos:

* TERCERO_000001
* TERCERO_000002
* TERCERO_000003

Información protegida:

* nombres reales
* contactos
* documentos

---

## Exportación de Datasets

Formatos:

* Parquet

Datasets generados:

* libro_mayor_2025_anon.parquet
* dim_terceros.parquet

---

# Sistema de Validaciones

Ubicación:

src/validations/

## Validaciones Críticas

* validate_required_columns
* validate_dates
* validate_debe_haber
* validate_codigo_cuenta
* validate_nombre_cuenta
* validate_fecha_datetime
* validate_puc_structure
* validate_account_hierarchy_consistency
* validate_valor_movimiento
* validate_data_types
* validate_value_ranges

Resultado:

La ejecución se detiene ante errores críticos.

---

## Validaciones Warning

* validate_nulls
* validate_empty_dataframe
* validate_duplicates
* validate_matching_coverage
* validate_ambiguous_third_parties
* validate_unmatched_third_parties

Resultado:

Las advertencias quedan registradas sin detener la ejecución.

---

# Calidad de Datos

Actualmente el pipeline monitorea:

* integridad contable
* calidad estructural
* calidad de terceros
* cobertura de matching
* ambigüedad de registros
* consistencia financiera
* trazabilidad de validaciones

Última ejecución:

* 252.266 movimientos procesados
* 11 validaciones críticas aprobadas
* 2 advertencias registradas

---

# Logging y Observabilidad

Ubicación:

src/logger.py

Implementado:

* logging centralizado
* trazabilidad de ejecución
* registro de errores
* registro de advertencias
* resumen consolidado de validaciones

Salida:

logs/pipeline.log

---

# Testing Automatizado

Framework:

pytest

Cobertura:

## Ingestión

* carga CSV
* carga Excel
* formatos inválidos
* archivos inexistentes

## Transformaciones

* limpieza financiera
* jerarquía contable
* calendario financiero

## Validaciones

* reglas contables
* tipos de datos
* calidad del dato
* jerarquía PUC

## Gobierno de Datos

* matching de terceros
* anonimización
* calidad de terceros

## Integración

* ejecución end-to-end del pipeline

Pruebas destacadas:

* test_pipeline_e2e.py
* test_anonymization.py
* test_third_party_governance.py

---

# Tecnologías Utilizadas

## Lenguaje

* Python 3.11

## Procesamiento

* Pandas

## Testing

* Pytest

## Persistencia

* Parquet

## Herramientas

* Git
* GitHub
* VS Code
* Jupyter Notebook

---

# Resultados Actuales

Movimientos financieros procesados:

* 252.266

Terceros evaluados:

* 14.009

Cobertura de matching:

* 97,58%

Validaciones críticas:

* 11 aprobadas

Datasets anonimizados:

* Sí

Gobierno de datos:

* Implementado

Dimensiones analíticas:

* Implementadas

------

## Semana 8 — Construcción de la Gold Layer

Objetivo:

Transformar la información validada, enriquecida y gobernada de la Silver Layer en estructuras analíticas preparadas para Business Intelligence, Financial Analytics y Power BI.

Componentes planificados:

### Fact_Movimientos

Tabla central de hechos financieros que almacenará:

* debe
* haber
* valor_movimiento

relacionada con dimensiones analíticas.

### Dim_Cuentas

Dimensión contable basada en la jerarquía PUC:

* codigo_cuenta
* nombre_cuenta
* clase
* grupo
* cuenta_puc
* subcuenta

### Dim_Tiempo

Dimensión temporal para análisis financiero:

* fecha
* anio
* mes
* trimestre
* semestre
* periodo_contable

### Dim_Terceros

Reutilización de la dimensión construida durante la Semana 7.

### KPIs Financieros

Construcción inicial de indicadores para:

* ingresos
* gastos
* resultado financiero
* análisis por tercero
* concentración de clientes
* concentración de proveedores

Resultado esperado:

Implementar un modelo estrella financiero preparado para reportería, análisis y consumo en Power BI.