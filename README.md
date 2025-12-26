# Electoral Evolution Visualization - Córdoba Capital

Sistema de análisis y visualización de la evolución electoral en las 14 seccionales de Córdoba Capital (2021-2025).

## 🎯 Objetivo

Analizar la evolución del voto y las fuerzas políticas en Córdoba Capital mediante:
- Visualización geográfica interactiva (mapas coropléticos)
- Análisis de tendencias temporales
- Insights politológicos (volatilidad, competitividad, patrones espaciales)

## 📊 Datos

- **Elecciones**: 2021, 2023, 2025 (Diputados)
- **Unidad geográfica**: 14 seccionales de Córdoba Capital
- **Fuentes**:
  - Datos electorales: Excel files con resultados por seccional
  - Límites geográficos: GeoJSON con 120 circuitos electorales

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio (si aplica)
# cd pyoclaude

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Procesar Datos

```bash
# Ejecutar pipeline ETL
python -m src.etl
```

### 3. Generar Visualizaciones

```bash
# Abrir notebooks de análisis
jupyter notebook

# O generar mapas directamente
python -m src.visualization.maps
```

## 📁 Estructura del Proyecto

```
pyoclaude/
├── data/
│   ├── raw/                    # Datos originales (Excel + GeoJSON)
│   ├── processed/              # Datos limpios (CSV, DB, GeoJSON)
│   └── mappings/               # Diccionarios de normalización
│
├── src/
│   ├── etl/                    # Extract-Transform-Load
│   ├── analysis/               # Análisis politológico
│   ├── visualization/          # Mapas y gráficos
│   └── config/                 # Configuración
│
├── notebooks/                  # Jupyter notebooks
├── outputs/                    # Mapas, reportes, figuras
├── tests/                      # Tests unitarios
│
├── CLAUDE.md                   # Guía para Claude Code
├── PLAN_PROYECTO.md            # Plan detallado del proyecto
└── requirements.txt            # Dependencias Python
```

## 🔧 Tecnologías

- **Python 3.10+**
- **Pandas / GeoPandas**: Procesamiento de datos
- **Folium**: Mapas interactivos
- **Plotly**: Gráficos interactivos
- **SQLite**: Base de datos
- **Jupyter**: Análisis exploratorio

## 📈 Análisis Disponibles

- **Evolución temporal**: Tendencias de voto por agrupación
- **Volatilidad electoral**: Índice de Pedersen
- **Seccionales competitivas**: Zonas de mayor disputa
- **Patrones geográficos**: Clustering espacial
- **Comparaciones inter-elecciones**: Cambios entre 2021-2023-2025

## 📝 Agrupaciones Políticas Principales

- JUNTOS POR EL CAMBIO
- HACEMOS POR CÓRDOBA
- LA LIBERTAD AVANZA
- UNIÓN POR LA PATRIA
- FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD

## 🤝 Contribuir

Para desarrolladores que trabajen en este proyecto:
1. Leer `CLAUDE.md` para contexto técnico
2. Revisar `PLAN_PROYECTO.md` para arquitectura completa
3. Seguir el flujo ETL → Análisis → Visualización

## 📚 Referencias

- [Datos Abiertos Argentina](https://datosgobar.github.io/paquete-apertura-datos/datasets-especificaciones/elecciones/)
- [Open Data Córdoba](https://github.com/OpenDataCordoba)
- Proyectos similares: Ver `PLAN_PROYECTO.md` sección "Referencias"

## 📄 Licencia

[Especificar licencia según corresponda]

## 👤 Autor

Proyecto de análisis electoral - Córdoba Capital 2026
