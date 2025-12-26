# Plan de Proyecto: Visualización Electoral Córdoba Capital

## 📊 Resumen del Proyecto
Sistema de análisis y visualización de la evolución electoral en las 14 seccionales de Córdoba Capital para los años 2021, 2023 y 2025.

---

## 🔍 Análisis de Datos Existentes

### Datos Electorales

#### 2021 (2021_porseccional_diputados.xls)
- **Registros**: 98
- **Columnas**: año, cargo, seccional, agrupacion, sum_diputados
- **Problema**: Usa "Seccinal" (typo)
- **Seccionales**: 14 (Seccinal 1-14)

#### 2023 (2023_porseccional_diputados.xlsx)
- **Registros**: 70
- **Columnas**: año, cargo, seccional, agrupacion, votos
- **Problema**: Mezcla "Seccinal" y "Seccional"
- **Seccionales**: 14 (Seccinal 1-10, Seccional 10)

#### 2025 (2025_porseccional_diputados.xlsx)
- **Registros**: 253
- **Columnas**: año, cargo, seccional, agrupacion, votos
- **Problema**: Usa "SECC" con nombres en texto (SECC PRIMERA, SECC SEGUNDA, etc.) y números (SECC 11-14)
- **Incluye**: 1 registro con "Seccional" sin número (posible total)

### Datos Geográficos

#### Seccionales_Circuitos.geojson
- **Features**: 120 (circuitos electorales)
- **Seccionales**: 14 (números 1-14)
- **Propiedades clave**:
  - `Seccional`: "1" a "14"
  - `Circuito`: identificador del circuito (ej: "14P")
  - `Nombre`: descripción completa
  - `Descripcion`: nombre del barrio
  - `union`: "Seccional X"
- **Distribución**: Varía de 1 circuito (Secc 1-3) hasta 18 circuitos (Secc 14)

### Agrupaciones Políticas Principales

**2021:**
1. JUNTOS POR EL CAMBIO (405,984 votos)
2. HACEMOS POR NUESTRO PAIS - HACEMOS POR CORDOBA (163,054)
3. FRENTE DE TODOS/UNION POR LA PATRIA (60,805)
4. ENCUENTRO VECINAL CORDOBA (44,706)
5. FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD (36,774)
6. LA LIBERTAD AVANZA (17,777)

**2023:**
1. LA LIBERTAD AVANZA (266,194) ⬆️
2. HACEMOS POR NUESTRO PAIS (256,912)
3. JUNTOS POR EL CAMBIO (195,251)
4. FRENTE DE TODOS/UNION POR LA PATRIA (96,142)
5. FRENTE DE IZQUIERDA (23,088)

**2025:** (datos disponibles pero con formato inconsistente)

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico Recomendado

#### Backend & ETL
- **Python 3.10+**
- **Pandas**: Procesamiento de datos electorales
- **GeoPandas**: Manipulación de datos geoespaciales
- **SQLite/PostgreSQL**: Almacenamiento de datos normalizados

#### Visualización
- **Folium**: Mapas interactivos con Leaflet.js
- **Plotly**: Gráficos interactivos y dashboards
- **Dash** (opcional): Framework para dashboards completos
- **Google Maps API** (si se requiere): Alternativa a Folium

#### Análisis Político
- **Scikit-learn**: Clustering de patrones electorales
- **Statsmodels**: Análisis de tendencias y correlaciones

#### Control de Versiones & Documentación
- **Git**: Control de versiones
- **Jupyter Notebooks**: Análisis exploratorio y reportes

---

## 📁 Estructura del Proyecto Propuesta

```
pyoclaude/
├── data/
│   ├── raw/                           # Datos originales (sin modificar)
│   │   ├── 2021_porseccional_diputados.xls
│   │   ├── 2023_porseccional_diputados.xlsx
│   │   ├── 2025_porseccional_diputados.xlsx
│   │   └── Seccionales_Circuitos.geojson
│   ├── processed/                     # Datos procesados
│   │   ├── electoral_data_clean.csv   # Datos limpios unificados
│   │   ├── seccionales_geo.geojson    # GeoJSON simplificado por seccional
│   │   └── electoral_database.db      # SQLite con datos normalizados
│   └── mappings/                      # Archivos de mapeo
│       ├── seccional_names.json       # Normalización de nombres
│       └── party_colors.json          # Colores por agrupación política
│
├── src/
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── extract.py                 # Lectura de archivos Excel/GeoJSON
│   │   ├── transform.py               # Limpieza y normalización
│   │   ├── load.py                    # Carga a base de datos
│   │   └── utils.py                   # Utilidades de mapeo
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── electoral_trends.py        # Análisis de tendencias
│   │   ├── political_analysis.py      # Análisis politológico
│   │   └── statistics.py              # Métricas y estadísticas
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── maps.py                    # Mapas coropléticos
│   │   ├── charts.py                  # Gráficos de tendencias
│   │   └── dashboard.py               # Dashboard integrado
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py                # Configuración general
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb  # Análisis exploratorio inicial
│   ├── 02_data_cleaning.ipynb         # Proceso de limpieza
│   ├── 03_electoral_evolution.ipynb   # Evolución electoral
│   └── 04_political_insights.ipynb    # Insights politológicos
│
├── outputs/
│   ├── maps/                          # Mapas generados
│   ├── reports/                       # Reportes HTML/PDF
│   └── figures/                       # Gráficos estáticos
│
├── tests/
│   ├── test_etl.py
│   ├── test_analysis.py
│   └── test_visualization.py
│
├── requirements.txt
├── setup.py
├── .gitignore
├── CLAUDE.md                          # Guía para Claude Code
└── README.md                          # Documentación del proyecto
```

---

## 🔄 Pipeline ETL (Extract-Transform-Load)

### 1. Extracción (Extract)

```python
# Pseudocódigo
def extract_electoral_data():
    # Leer Excel con encoding correcto
    df_2021 = pd.read_excel('2021_porseccional_diputados.xls', encoding='latin-1')
    df_2023 = pd.read_excel('2023_porseccional_diputados.xlsx')
    df_2025 = pd.read_excel('2025_porseccional_diputados.xlsx')

    # Leer GeoJSON
    gdf_circuitos = gpd.read_file('Seccionales_Circuitos.geojson')

    return df_2021, df_2023, df_2025, gdf_circuitos
```

### 2. Transformación (Transform)

**Problemas a resolver:**

#### A. Normalización de nombres de seccionales

```python
SECCIONAL_MAPPING = {
    # 2021/2023
    'Seccinal 1': '1', 'Seccional 1': '1',
    'Seccinal 2': '2', 'Seccional 2': '2',
    # ... hasta 14

    # 2025
    'SECC PRIMERA': '1',
    'SECC SEGUNDA': '2',
    'SECC TERCERA': '3',
    'SECC CUARTA': '4',
    'SECC QUINTA': '5',
    'SECC SEXTA': '6',
    'SECC SEPTIMA': '7',
    'SECC OCTAVA': '8',
    'SECC NOVENA': '9',
    'SECC DECIMA': '10',
    'SECC 11': '11',
    'SECC 12': '12',
    'SECC 13': '13',
    'SECC 14': '14',
    'Seccional': None  # Registro de total, excluir
}
```

#### B. Normalización de nombres de columnas

```python
COLUMN_MAPPING = {
    'sum_diputados': 'votos',  # 2021 usa diferente nombre
    'año': 'anio',
    'agrupacion': 'agrupacion',
    'seccional': 'seccional'
}
```

#### C. Normalización de nombres de agrupaciones

```python
PARTY_MAPPING = {
    'HACEMOS POR NUESTRO PAIS  - HACEMOS POR CORDOB': 'HACEMOS POR CÓRDOBA',
    'FRENTE DE TODOS/UNION POR LA PATRIA': 'UNIÓN POR LA PATRIA',
    # ... otros
}
```

#### D. Agregación de GeoJSON por Seccional

```python
# Convertir 120 circuitos → 14 seccionales
gdf_seccionales = gdf_circuitos.dissolve(by='Seccional')
```

### 3. Carga (Load)

**Esquema de base de datos:**

```sql
-- Tabla de seccionales
CREATE TABLE seccionales (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    geometry TEXT NOT NULL  -- GeoJSON
);

-- Tabla de agrupaciones políticas
CREATE TABLE agrupaciones (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    nombre_corto TEXT,
    color TEXT
);

-- Tabla de resultados electorales
CREATE TABLE resultados (
    id INTEGER PRIMARY KEY,
    anio INTEGER NOT NULL,
    cargo TEXT NOT NULL,
    seccional_id INTEGER NOT NULL,
    agrupacion_id INTEGER NOT NULL,
    votos INTEGER NOT NULL,
    FOREIGN KEY (seccional_id) REFERENCES seccionales(id),
    FOREIGN KEY (agrupacion_id) REFERENCES agrupaciones(id)
);

-- Índices
CREATE INDEX idx_resultados_anio ON resultados(anio);
CREATE INDEX idx_resultados_seccional ON resultados(seccional_id);
```

---

## 📊 Componentes de Visualización

### 1. Mapa Coroplético Interactivo (Folium)

**Funcionalidades:**
- Selector de año (2021, 2023, 2025)
- Selector de agrupación política
- Coloreado por porcentaje de votos
- Popup con detalles al hacer clic
- Leyenda dinámica

```python
# Ejemplo conceptual
map = folium.Map(location=[-31.4201, -64.1888], zoom_start=12)

folium.Choropleth(
    geo_data=seccionales_geojson,
    data=electoral_df,
    columns=['seccional', 'porcentaje_votos'],
    key_on='feature.properties.Seccional',
    fill_color='YlOrRd',
    legend_name='Porcentaje de Votos'
).add_to(map)
```

### 2. Dashboard de Evolución Temporal (Plotly/Dash)

**Gráficos:**
- Línea de tiempo: Evolución de votos por agrupación
- Barras apiladas: Composición por seccional
- Heatmap: Cambios entre elecciones
- Scatter: Correlaciones entre seccionales

### 3. Análisis Politológico

**Métricas a calcular:**
- Volatilidad electoral (cambio neto entre elecciones)
- Concentración de votos (índice de Herfindahl)
- Seccionales "swing" (mayor variabilidad)
- Patrones geográficos (clustering espacial)

---

## 🎯 Plan de Implementación

### Fase 1: Setup & ETL (Prioridad Alta)
1. ✅ Configurar estructura de proyecto
2. ✅ Crear archivos de mapeo (seccionales, partidos)
3. ✅ Implementar pipeline ETL completo
4. ✅ Validar datos procesados

### Fase 2: Análisis Exploratorio (Prioridad Alta)
1. ✅ Notebook de exploración de datos
2. ✅ Identificar patrones y anomalías
3. ✅ Calcular estadísticas descriptivas

### Fase 3: Visualización Básica (Prioridad Media)
1. ✅ Mapa coroplético básico (un año)
2. ✅ Gráfico de barras por seccional
3. ✅ Línea de tiempo de evolución

### Fase 4: Dashboard Interactivo (Prioridad Media)
1. ⬜ Integrar múltiples visualizaciones
2. ⬜ Agregar selectores interactivos
3. ⬜ Implementar comparaciones lado a lado

### Fase 5: Análisis Avanzado (Prioridad Baja)
1. ⬜ Clustering de seccionales similares
2. ⬜ Análisis de tendencias predictivas
3. ⬜ Reportes automatizados

---

## 📚 Referencias y Recursos

### Proyectos Similares Encontrados en GitHub

#### Datos Electorales de Argentina:
- [matuteiglesias/elecciones-ARG](https://github.com/matuteiglesias/elecciones-ARG) - Datos y código para elecciones Argentina 2025
- [tartagalensis/circuitos_electorales_AR](https://github.com/tartagalensis/circuitos_electorales_AR) - Circuitos electorales en GeoJSON
- [electorArg/PolAr_Data](https://github.com/electorArg/PolAr_Data) - Repositorio de datos electorales desde 2007
- [PoliticaArgentina/data_warehouse](https://github.com/PoliticaArgentina/data_warehouse) - Datos políticos con GIS

#### Herramientas de Análisis Político:
- [poliscipy/poliscipy](https://github.com/poliscipy/poliscipy) - Librería Python para análisis político
- [pollsposition/dashboards](https://github.com/pollsposition/dashboards) - Dashboards electorales con PyMC3

#### Visualización:
- [python-visualization/folium](https://github.com/python-visualization/folium) - Mapas interactivos
- [Folium Choropleth Examples](https://python-visualization.github.io/folium/latest/user_guide/geojson/choropleth.html)
- [Plotly Choropleth Maps](https://plotly.com/python/choropleth-maps/)

### Documentación Clave:
- Datos Abiertos Argentina: https://datosgobar.github.io/paquete-apertura-datos/datasets-especificaciones/elecciones/
- Open Data Córdoba: https://github.com/OpenDataCordoba

---

## 🔑 Conceptos Clave de Análisis Politológico

### Volatilidad Electoral
Mide el cambio neto en el apoyo a diferentes partidos entre elecciones.

```python
# Pedersen Index
volatilidad = 0.5 * sum(abs(votos_t1 - votos_t0))
```

### Seccionales Competitivas
Identificar zonas con mayor disputa electoral (diferencia pequeña entre 1er y 2do lugar).

### Geografía Electoral
Identificar patrones espaciales (¿las seccionales cercanas votan similar?)

---

## 💡 Insights Preliminares Observados

1. **Crecimiento de La Libertad Avanza**: De 17k votos (2021) a 266k (2023) - crecimiento exponencial
2. **Caída de Juntos por el Cambio**: De 406k (2021) a 195k (2023)
3. **Estabilidad de Hacemos por Córdoba**: Mantiene ~250k votos
4. **Datos 2025**: Mayor granularidad (253 registros vs 70-98 de años anteriores)

---

## ⚠️ Consideraciones Importantes

### Calidad de Datos
- Verificar que los totales por seccional coincidan con datos oficiales
- Validar que no haya duplicados
- Confirmar que "Seccional" sin número en 2025 sea un total a excluir

### Normalización
- Crear diccionario maestro de nombres de agrupaciones
- Documentar todos los cambios de nomenclatura
- Mantener trazabilidad de transformaciones

### Performance
- Para 120 polígonos, Folium debería funcionar bien
- Si se agregan más capas, considerar simplificación de geometrías
- Cachear datos procesados para visualizaciones rápidas

---

## 🚀 Próximos Pasos Inmediatos

1. **Crear requirements.txt** con dependencias
2. **Implementar ETL básico** (extract.py, transform.py, load.py)
3. **Generar archivo unificado** electoral_data_clean.csv
4. **Crear GeoJSON simplificado** por seccional (no circuitos)
5. **Primer mapa**: Coroplético de resultados 2023
