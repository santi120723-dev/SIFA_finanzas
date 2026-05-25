# SIFA_finanzas-Pipeline_ETL_para_Finanzas_(Python+Pandas)

## Resumen Ejecutivo
Este proyecto implementa un pipeline ETL modular orientado a datos financieros reales utilizando Python y Pandas. El sistema procesa libros mayores heterogéneos mediante una arquitectura Medallion (Bronze → Silver → Gold), incorporando validaciones contables, limpieza reusable, logging centralizado y pruebas end-to-end sobre datasets reales.

Durante esta etapa el proyecto evolucionó desde una estructura inicial de ingesta hacia un pipeline más desacoplado y preparado para escenarios reales de integración ETL y Business Intelligence financiero.

---

## Descripción
Proyecto enfocado en transformar datasets contables inconsistentes en información estructurada, validada y reutilizable para futuros procesos analíticos y dashboards financieros.

Actualmente incluye:

- Pipeline ETL modular:
Separación clara entre ingestión, limpieza, validación y preparación analítica.

- Arquitectura Medallion:
Organización de datasets en capas Bronze, Silver y preparación inicial de Gold.

- Validaciones financieras:
Implementación de reglas básicas de integridad contable como validación Debe = Haber.

- Limpieza reusable:
Funciones desacopladas para normalización de columnas, manejo de nulos y estandarización estructural.

- Testing e integración:
Pruebas sobre datasets financieros reales utilizando notebooks y testing automatizado con pytest.

---

## Estado del Proyecto

### Implementado (Funcional)

#### Arquitectura Medallion
- Directorios definidos:
  - data/bronze/
  - data/silver/
  - data/gold/

- Separación por dominios:
  - accounting/
  - inventory/
  - manufacturing/

- Configuración centralizada mediante `src/config.py`.

- Uso de `pathlib.Path` para manejo robusto de rutas.

---

#### Capa Bronze (Ingestion)

##### Funcionalidades implementadas
- `load_file()` en `src/ingestion/extract.py`
- Lectura de archivos:
  - `.xlsx`
  - `.csv`
  - `.txt`

##### Validaciones iniciales
- Archivo existente.
- Formato soportado.
- DataFrame no vacío.
- Logging automático de errores.

##### Mejoras implementadas
- Integración correcta desde notebooks.
- Compatibilidad con rutas absolutas.
- Eliminación de hardcoding de rutas.

---

#### Capa Silver (Transformación y limpieza)

##### Limpieza reusable implementada
Archivo:
`src/utils/cleaning.py`

Funciones actuales:
- normalización de nombres de columnas
- limpieza de strings
- manejo de valores nulos
- estandarización estructural
- preparación reusable de DataFrames financieros

##### Normalización financiera
Archivo:
`src/preprocess/normalizer.py`

- `normalize_libro_mayor()`
- integración desacoplada de reglas de transformación
- preparación estructural previa a validaciones

---

#### Validaciones financieras

Archivo:
`src/validations/business_rules.py`

##### Implementado
- `validate_debe_haber()`

##### Funcionalidad
- Validación de integridad contable:
  - suma Debe ≈ suma Haber
- manejo de tolerancia configurable
- manejo explícito de errores
- logging de diferencias detectadas

##### Validaciones estructurales
- columnas requeridas
- datasets incompletos
- errores de integración ETL

---

#### Logging y trazabilidad

Archivo:
`src/logger.py`

##### Implementado
- logging centralizado
- salida en:
  - consola
  - `logs/pipeline.log`
- timestamps automáticos
- registro de:
  - errores
  - warnings
  - ejecución del pipeline
  - métricas de procesamiento

---

#### Testing

##### Pytest
Carpeta:
`tests/`

##### Cobertura actual
- carga de archivos
- formatos inválidos
- archivos vacíos
- validaciones contables
- pruebas de integración iniciales

##### Fixtures de testing
- bronze_test.csv
- bronze_test.xlsx
- bronze_test_missing.xlsx

---

#### Integración Notebook + ETL

##### Implementado
- notebooks integrados al pipeline
- ejecución end-to-end:
  - Bronze → Normalize → Validate

##### Problemas resueltos
- `ModuleNotFoundError: No module named 'src'`
- manejo incorrecto de rutas relativas
- conflictos entre `str` y `Path`
- diferencias estructurales entre archivos Excel

---

### En desarrollo (Sin implementar completamente)

#### Capa Gold

##### Parcialmente preparada
- estructura `data/gold/`
- preparación para:
  - KPIs financieros
  - reporting
  - datasets analíticos

##### Pendiente
- exportación definitiva a Parquet/CSV
- modelo dimensional
- tablas analíticas
- métricas financieras

---

#### SQL analítico

##### Pendiente
- consultas SQL financieras
- agregaciones analíticas
- construcción de KPIs

---

#### Dashboards BI

##### Pendiente
- Power BI
- visualizaciones financieras
- reporting ejecutivo

---

## Tecnologías Utilizadas

### Core
- Python 3.11.7
- Pandas
- Pathlib
- Pytest

### Herramientas
- Git & GitHub
- VS Code
- Jupyter Notebook
- Logging estándar de Python

---

## Estructura del Proyecto

```text
SIFA_finanzas/

│
├── data/
│   ├── bronze/
│   │   ├── accounting/
│   │   │   └── libro_mayor_2025.xlsx
│   │   ├── inventory/
│   │   └── manufacturing/
│   │
│   ├── silver/
│   │   ├── accounting/
│   │   ├── inventory/
│   │   └── manufacturing/
│   │
│   └── gold/
│       ├── finance/
│       ├── management/
│       └── operations/
│
├── logs/
│   └── pipeline.log
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_test_cleaning.ipynb
│   └── 03_test_pipeline.ipynb
│
├── reports/
│
├── scripts/
│   └── generate_dummy_data.py
│
├── sql/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── config.py
│   ├── logger.py
│   │
│   ├── ingestion/
│   │   └── extract.py
│   │
│   ├── preprocess/
│   │   └── normalizer.py
│   │
│   ├── transformations/
│   │
│   ├── validations/
│   │   └── business_rules.py
│   │
│   ├── utils/
│   │   └── cleaning.py
│   │
│   └── orchestration/
│
├── tests/
│   ├── test_extract.py
│   ├── test_validations.py
│   └── test_cleaning.py
│
└── README.md
```

#### lecciones Aprendidas
- La complejidad real de un pipeline ETL muchas veces aparece durante la integración entre módulos y no únicamente en la transformación de datos.
- Los notebooks requieren manejo explícito de rutas y contexto del proyecto para integrarse correctamente con arquitecturas modulares.
- La separación de responsabilidades facilita debugging, testing y escalabilidad.
- La calidad de datos en pipelines financieros depende tanto de validaciones técnicas como de reglas contables.
- El uso de logging y testing automatizado mejora considerablemente la trazabilidad y mantenibilidad del sistema.

#### Próximos Pasos
* Finalizar la capa Silver
- Consolidar reglas reutilizables de limpieza.
- Mejorar validaciones estructurales.
- Añadir validaciones financieras adicionales.
* Desarrollar la capa Gold
- Exportar datasets analíticos a Parquet.
- Construir KPIs financieros.
- Preparar datasets para BI y reporting.
* Implementar SQL analítico
- Crear consultas financieras reutilizables.
- Construir agregaciones para análisis financiero.
* Integración BI
- Conectar Power BI a la capa Gold.
- Diseñar dashboards financieros iniciales.
* Mejorar testing
- Añadir pruebas end-to-end automatizadas.
- Incrementar cobertura de reglas de negocio.

#### Caso de Uso
Simulación de pipeline financiero orientado a Business Intelligence y análisis contable sobre datasets reales. El proyecto busca representar escenarios comunes de integración ETL financiera, calidad de datos y preparación analítica para reporting empresarial.