# SIFA_finanzas – Análisis de Datos Financieros (Python + Pandas)

---

## Descripción

Proyecto de análisis de datos financieros enfocado en la limpieza, transformación y exploración de información contable para su uso en procesos de análisis y Business Intelligence.

Actualmente se desarrolla una primera versión (v1) orientada a la construcción de un pipeline de datos reproducible.

---

## Resultado actual

Hasta el momento, el proyecto permite:

- Cargar datos financieros desde archivos Excel  
- Explorar la estructura del dataset  
- Identificar problemas de calidad de datos  
- Realizar procesos iniciales de limpieza en Python (Pandas)  
- Preparar un dataset base para análisis posteriores  

---

## Aprendizajes clave

Durante esta primera fase se identificó que los datos financieros presentan problemas de calidad que impactan directamente el análisis, entre ellos:

- Valores nulos en columnas relevantes  
- Inconsistencias en nombres de cuentas  
- Formatos no estandarizados  

Esto evidencia la importancia de la limpieza y transformación de datos como etapa fundamental antes de calcular KPIs o construir visualizaciones.

---

## Objetivo del proyecto

Desarrollar un flujo de trabajo que permita:

- Transformar datos financieros en información estructurada  
- Preparar datasets listos para análisis  
- Construir la base para KPIs financieros y dashboards  
- Simular un entorno real de análisis de datos aplicado a finanzas  

---

## Enfoque del análisis

El proyecto sigue un flujo estructurado de datos:

1. Ingesta de datos (Excel)  
2. Carga en Python (Pandas)  
3. Exploración del dataset  
4. Limpieza y estandarización  
5. Preparación para análisis y visualización  

---

## Trabajo técnico realizado

### 1. Carga de datos
- Lectura de archivos Excel con Pandas  
- Validación inicial del dataset  

### 2. Exploración de datos
- Revisión de columnas y tipos de datos  
- Detección de valores nulos e inconsistencias  

### 3. Limpieza de datos
- Ajustes iniciales en la estructura del dataset  
- Preparación de la información para análisis  

---

## Estado del proyecto

### ✔ Implementado
- Carga de datos desde Excel  
- Exploración del dataset  
- Limpieza inicial de datos  
- Estructuración básica del entorno de análisis  

### En progreso
- Limpieza y transformación más profunda  
- Estandarización de variables contables  
- Organización del pipeline en scripts reutilizables  

### Próximas etapas
- Cálculo de KPIs financieros  
- Análisis exploratorio completo (EDA)  
- Consultas SQL  
- Desarrollo de dashboard en Power BI  

---

## Tecnologías utilizadas

- Python (Pandas)  
- Jupyter Notebook  
- Excel  
- Git & GitHub  
- VS Code  

---

## Estructura del proyecto

SIFA_finanzas/

- src/
  Scripts de procesamiento y lógica del pipeline.

- notebooks/
  Análisis exploratorio (EDA inicial).

- data/
  - raw/
    Datos originales en Excel.
  - clean/
    Datos procesados y limpios.

- reports/
  Resultados de análisis y salidas del proyecto.

- sql/
  Consultas SQL utilizadas en el análisis.

- dashboard/
  Visualizaciones en Power BI.

- README.md
  Documentación principal del proyecto.

---

## Aplicación del proyecto

Este proyecto simula un caso real de análisis financiero donde los datos requieren ser limpiados y estructurados antes de generar valor analítico.

Se enfoca en el desarrollo de habilidades en:

- Preparación y limpieza de datos  
- Análisis exploratorio  
- Procesamiento de información financiera  
- Fundamentos de Business Intelligence  

---