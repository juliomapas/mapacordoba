# Dashboard Electoral Córdoba Capital

Aplicación web interactiva para visualizar la evolución electoral de Córdoba Capital en 2021, 2023 y 2025.

---

## 🚀 Inicio Rápido

### 1. Ejecutar la aplicación

```bash
python app.py
```

### 2. Abrir en navegador

```
http://127.0.0.1:8050/
```

### 3. Detener servidor

Presiona `Ctrl+C` en la terminal

---

## 📊 Características

### Componentes Principales

**1. Mapa Electoral Interactivo**
- Visualización por seccional con colores por partido ganador
- Slider para navegar entre 2021, 2023, 2025
- Hover para ver datos detallados (partido, votos, porcentaje)
- Etiquetas permanentes por seccional

**2. Métricas Clave**
- Total de votos del año seleccionado
- Partido ganador a nivel ciudad
- Seccionales ganadas por el líder
- Año actualmente visualizado

**3. Distribución de Votos**
- Gráfico de torta: Top 5 partidos
- Gráfico de barras: Votos por partido

**4. Evolución Temporal**
- Líneas de tendencia 2021 → 2023 → 2025
- Top 5 partidos por total de votos
- Marca visual del año seleccionado

**5. Tabla Comparativa**
- Ganador por seccional en cada año
- Vista de cambios electorales

---

## 🎨 Paleta de Colores

```
LA LIBERTAD AVANZA       → #9370DB (Violeta)
JUNTOS POR EL CAMBIO     → #FFD700 (Amarillo)
HACEMOS POR CÓRDOBA      → #87CEEB (Celeste)
UNIÓN POR LA PATRIA      → #0047AB (Azul)
FRENTE DE IZQUIERDA      → #DC143C (Rojo)
```

---

## 📁 Estructura

```
app.py                      # Aplicación principal
data/
  ├── raw/                  # Datos originales
  │   ├── Seccionales_Circuitos.geojson
  │   ├── 2021_porseccional_diputados.xls
  │   ├── 2023_porseccional_diputados.xlsx
  │   └── 2025_porseccional_diputados.xlsx
  └── processed/            # Datos procesados
      ├── electoral_data_clean.csv
      ├── electoral_database.db
      └── seccionales_geo.geojson
```

---

## 🔧 Dependencias

```
dash==3.3.0
dash-bootstrap-components==2.0.4
plotly==6.5.0
pandas
geopandas
```

Instalar:
```bash
pip install dash dash-bootstrap-components plotly pandas geopandas
```

---

## 💡 Uso

### Navegación

1. **Cambiar de año:** Usa el slider debajo del mapa
2. **Ver detalles:** Pasa el mouse sobre una seccional
3. **Analizar evolución:** Observa el gráfico de líneas
4. **Comparar:** Revisa la tabla al final

### Interpretación

**2021:** Dominio de JUNTOS POR EL CAMBIO (amarillo)
**2023:** Fragmentación - LA LIBERTAD AVANZA irrumpe (violeta)
**2025:** Consolidación de ALIANZA LA LIBERTAD AVANZA (violeta)

---

## 🐛 Resolución de Problemas

**Error: ModuleNotFoundError**
```bash
pip install dash dash-bootstrap-components
```

**Error: No se encuentra el archivo**
```bash
# Verificar que estás en el directorio del proyecto
python -m src.etl  # Regenerar datos procesados
```

**Puerto 8050 ocupado**
```python
# En app.py, cambiar:
app.run_server(debug=True, port=8051)
```

---

## 📝 Personalización

### Cambiar colores

Edita el diccionario `PARTY_COLORS` en `app.py`:

```python
PARTY_COLORS = {
    'LA LIBERTAD AVANZA': '#TU_COLOR_AQUI',
    # ...
}
```

### Cambiar puerto

```python
app.run_server(debug=True, port=TU_PUERTO)
```

### Agregar más años

1. Agregar datos en `data/raw/`
2. Ejecutar ETL: `python -m src.etl`
3. Actualizar marks del slider en `app.py`

---

## 🌐 Deployment

### Opciones de despliegue

**1. Render.com** (Recomendado)
- Gratuito para proyectos públicos
- Deploy automático desde GitHub

**2. Heroku**
- Free tier disponible
- Requiere Procfile

**3. PythonAnywhere**
- Fácil configuración
- Free tier limitado

**4. Docker**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 📈 Próximas Mejoras

- [ ] Exportar datos a CSV/Excel
- [ ] Filtros por partido
- [ ] Mapas de calor (swing electoral)
- [ ] Descarga de gráficos como PNG
- [ ] Modo oscuro
- [ ] Comparación lado a lado de 2 años
- [ ] Análisis de competitividad por seccional

---

## 📄 Licencia

Proyecto educativo - Libre uso

---

**Desarrollado con:**
- Python 3.11+
- Dash by Plotly
- GeoPandas
- Bootstrap 5

**Última actualización:** 2025-12-25
