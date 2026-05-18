# SIFA_finanzas-Pipeline_ETL_para_Finanzas_(Python+Pandas)
## Resumen Ejecutivo
Este proyecto implementa un pipeline ETL modular para procesar datos contables heterogéneos (Excel, CSV y TXT) y generarlos en un formato estructurado listo para análisis financiero. Utiliza una arquitectura Medallion (Bronze → Silver → Gold) para asegurar trazabilidad y escalabilidad del sistema.

## Descripción
Proyecto centrado en la transición de datos contables discontinuos a información útil para toma de decisiones. Incluye:

- Extracción y validación básica: Carga de archivos y revisión inicial de integridad.
- Estructura profesional: Modularización del código y jerarquía de capas (Bronze/Silver/Gold).
- Fundamento para BI: Preparación de datos para futuros análisis como KPIs y modelos en estrella.

## Estado del Proyecto
#### Implementado (Funcional)
* Arquitectura Medallion:
- Directorios definidos: data/bronze/, data/silver/, data/gold/.
- Capa Bronze: Contiene archivos de origen en Excel, CSV y TXT.
- Configuración centralizada: src/config.py usa pathlib para manejar rutas.
- Logging: Sistema en src/logger.py que escribe en logs/pipeline.log y consola.

#### Capa de extracción (Ingestion):
- Función load_file() en src/ingestion/extract.py que carga archivos soportados (.xlsx, .csv, .txt).
- Validaciones: Existencia del archivo, formato válido y DataFrame no vacío.
- Manejo de errores con logging automático.
- Uso de type hints para garantizar robustez.

#### Modularidad:
- Estructura en módulos: ingestion/, transformations/, validations/, utils/, orchestration/.
- Rutas absolutas para evitar hardcoding.

### En desarrollo (Sin implementar)
### Capa de transformación (Silver):
- Carpeta src/transformations/ existe, pero no contiene código.
- Objetivo pendiente: Limpieza (normalización de columnas, fechas), validaciones contables (ej. Debe = Haber).

#### Validaciones contables:
Reglas definidas en comentarios (ej. consistencia de saldos), pero no implementadas en código.

#### Capa de carga (Gold):
Sin desarrollo: No existen módulos para exportar datos a data/gold/ ni integrar con bases de datos.

## Tecnologías Utilizadas
Core: Python 3.x, Pandas, Pathlib.
Tools: Git y GitHub para control de versiones, VS Code, Logging estándar de Python.

## Estructura del Proyecto

```text
SIFA_finanzas/
    data/
        bronze/
            accounting/
                libro_mayor_2025.xlsx
            inventory/
                movimientos_inventario_2025.xlsx
            manufacturing/
                ordenes_fabricacion_2025.xlsx

        silver/
            accounting/
            inventory/
            manufacturing/

        gold/
            finance/
            management/
            operations/

    notebooks/

    src/
        config.py
        ingestion/
            extract.py
        transformations/
        validations/
        utils/
        orchestration/
        logger.py

    logs/
    sql/
    reports/
    README.md
```

## Lecciones Aprendidas
- La arquitectura modular permite escalar el sistema sin romper funcionalidades existentes.
- La capa Bronze ya es operativa, lo que provee una base sólida para futuras transformaciones.
- El logging facilita el seguimiento y depuración del proceso.

## Próximos Pasos
### Implementar la capa Silver:
- Escribir reglas de limpieza y validación en src/transformations/.
- Ejemplos: Estandarizar fechas (YYYY-MM-DD), limpiar nombres de columnas, validar integrity contable.

### Desarrollar la capa Gold:
- Exportar datos a Parquet o CSV en data/gold/.
- Crear un modelo en estrella (tabla de hechos + dimensiones).

### Automatizar el pipeline:
Integrar herramientas como Airflow para ejecuciones programadas.

## Caso de Uso
Simulación de pipeline para análisis financiero y BI en entornos contables reales.