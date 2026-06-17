# Gold Layer Design

## Objetivo

Transformar la información financiera validada y enriquecida de la Silver Layer en estructuras analíticas preparadas para:

- Financial Analytics
- Business Intelligence
- Reporting Financiero
- Power BI

La Gold Layer será la capa de consumo analítico del proyecto.

## Fact_Movimientos

Representa cada movimiento contable procesado.

### Métricas

- debe
- haber
- valor_movimiento

### Claves

- fecha
- codigo_cuenta
- tercero_id

## Dim_Cuentas

Contiene la jerarquía contable utilizada para análisis financieros.

### Campos

- codigo_cuenta
- nombre_cuenta
- clase
- grupo
- cuenta_puc
- subcuenta

## Dim_Terceros

Contiene la clasificación de terceros obtenida durante el proceso de matching.

### Campos

- tercero_id
- tipo_tercero
- estado_matching

## Dim_Tiempo

Dimensión temporal para análisis financieros.

### Campos

- fecha
- anio
- mes
- trimestre
- semestre
- periodo_contable

## Modelo Analítico

                    Dim_Tiempo
                         |
                         |
Dim_Cuentas ---- Fact_Movimientos ---- Dim_Terceros


## KPIs Iniciales

### Ingresos mensuales

### Gastos mensuales

### Resultado mensual

### Top clientes

### Top proveedores

### Concentración por tercero