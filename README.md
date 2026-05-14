### SIFA_finanzas – Análisis de Datos Financieros (Python + Pandas)
## Descripción
Proyecto de análisis de datos financieros enfocado en la limpieza, transformación y exploración de información contable, con enfoque en Business Intelligence  y análisis financiero.

Este proyecto forma parte de un proceso de transición profesional desde el área contable hacia el rol de Analista de Datos Financiero y Business Intelligence, aprovechando experiencia previa en contabilidad para fortalecer el análisis de datos y la toma de decisiones.
Actualmente, el proyecto evoluciona desde una versión exploratoria en Jupyter Notebook hacia una arquitectura estructurada basada en un pipeline de datos reproducible (ETL).

n esta segunda fase se inicia la construcción de la capa de extracción (Extract) de datos de forma modular y escalable.

## Objetivo del proyecto
Desarrollar un flujo de trabajo que permita:
    • Automatizar la carga de datos financieros desde múltiples fuentes 
    • Estandarizar la lectura de archivos contables 
    • Construir un pipeline de datos reproducible (ETL) 
    • Preparar datos para análisis financiero y Business Intelligence 
    • Simular un entorno real de análisis de datos aplicado a finanzas 

## Funcionalidades actuales
Hasta el momento, el proyecto permite:
    • Cargar datos desde archivos Excel, CSV y TXT 
    • Centralizar rutas mediante config.py 
    • Implementar una función genérica de carga en la capa ETL (src/extract.py) 
    • Validar existencia de archivos antes de la lectura 
    • Manejar errores básicos durante la carga de datos 
    • Convertir archivos en estructuras DataFrame con Pandas 

## Aprendizajes clave
Durante esta fase se evidenció la importancia de estructurar la carga de datos como un sistema reutilizable en lugar de código aislado en notebooks.

Desde la perspectiva de análisis financiero y Business Intelligence, se identifican principios clave:
    • Los datos contables provienen de múltiples formatos (Excel, CSV, TXT) 
    • La validación previa de información es esencial para garantizar confiabilidad 
    • Separar configuración y lógica mejora la escalabilidad del proyecto 
    • El manejo de errores es fundamental en pipelines de datos reales 
    • La carpeta src/ representa el núcleo del proceso ETL 
Esto refuerza la importancia de la extracción de datos como primera etapa crítica en cualquier proceso de análisis financiero.

## Trabajo técnico realizado
1. Configuración del sistema
    • Creación de config.py para gestión centralizada de rutas 
    • Eliminación de rutas hardcodeadas 
    • Organización de archivos contables del proyecto 
2. Capa de extracción (Extract)
    • Implementación de función genérica load_file() en src/extract.py 
    • Lectura de archivos en múltiples formatos 
    • Uso de Pandas para conversión a DataFrame 
    • Estandarización del proceso de carga de datos 
3. Manejo de datos
    • Validación de existencia de archivos 
    • Control de errores durante la carga 
    • Preparación de datasets para análisis posterior 

## Estado del proyecto
✔ Implementado
    • Configuración centralizada de rutas 
    • Carga de archivos financieros (Excel, CSV, TXT) 
    • Capa de extracción reutilizable 
    • Manejo básico de errores 
    • Estructura modular del proyecto 
En progreso
    • Validación más profunda de datos contables 
    • Inicio de la fase de transformación (Transform) 
    • Estandarización de variables financieras 
    • Preparación de datasets limpios para análisis 
Próximas etapas
    • Limpieza estructurada de datos financieros 
    • Cálculo de KPIs contables 
    • Reglas de consistencia (Debe = Haber) 
    • Análisis exploratorio de datos (EDA) 
    • Desarrollo de dashboard en Power BI 

## Tecnologías utilizadas
    • Python (Pandas) 
    • Jupyter Notebook 
    • Excel 
    • Git & GitHub 
    • VS Code

## Estructura del proyecto
SIFA_finanzas/
* data/
   - raw/ (Fuentes: libro_mayor_2025.xlsx, etc.)
   - staging/
   - clean/
* notebooks/
   - 01_carga_datos.ipynb
* reports/
* src/
   - config.py
   - extract.py
   - main.py
* tests/
* README.md

## Aplicación del proyecto
Este proyecto simula un caso real de análisis financiero donde los datos provienen de múltiples fuentes y deben ser estructurados antes de generar valor analítico.
Se enfoca en el desarrollo de habilidades clave para el rol de Analista de Datos Financiero y Business Intelligence, integrando experiencia previa en contabilidad con herramientas de análisis de datos.

## Habilidades desarrolladas:
    • Ingeniería básica de datos 
    • Preparación y carga de datos financieros 
    • Manejo de archivos contables heterogéneos 
    • Construcción de pipelines de datos (ETL) 
    • Fundamentos de Business Intelligence 

## Cierre profesional
Este proyecto representa un paso en la transición hacia roles enfocados en análisis de datos, donde el objetivo es pasar de la operación contable tradicional al uso de datos para la toma de decisiones estratégicas y generación de valor empresarial.