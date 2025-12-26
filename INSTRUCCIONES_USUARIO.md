# Instrucciones para el Usuario - Sistema Electoral Córdoba

## ✅ Estado Actual del Sistema

El sistema está completamente funcional y procesando datos normalizados correctamente.

### Datos Procesados:
- **420 registros** de 3 elecciones (2021, 2023, 2025)
- **14 seccionales** (Seccional 1 hasta Seccional 14)
- **24 agrupaciones políticas**

---

## 🚀 Cómo Ejecutar la Aplicación

### Método 1: Scripts Automáticos (Recomendado - Windows)

1. **Primera vez** (instalar dependencias):
   ```cmd
   setup.bat
   ```

2. **Ejecutar la aplicación**:
   ```cmd
   run.bat
   ```

3. **Abrir navegador**:
   - Ir a: `http://127.0.0.1:8050`

### Método 2: Manual

1. **Activar entorno virtual**:
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Ejecutar aplicación**:
   ```bash
   python app.py
   ```

3. **Abrir navegador**:
   - Ir a: `http://127.0.0.1:8050`

---

## 📊 Formato de Datos Actualizado

### Los archivos Excel ahora usan formato normalizado:

#### Columnas requeridas:
- `año` (o `a�o`): Año de la elección
- `cargo`: Cargo electoral (ej: "DIPUTADOS NACIONALES")
- `seccional`: Nombre de la seccional (formato: "Seccional 1", "Seccional 2", etc.)
- `agrupacion`: Nombre de la agrupación política
- `diputados`: Cantidad de votos obtenidos

#### Ejemplo de datos:
```
año  | cargo                 | seccional    | agrupacion               | diputados
2021 | DIPUTADOS NACIONALES  | Seccional 1  | JUNTOS POR EL CAMBIO     | 5904
2021 | DIPUTADOS NACIONALES  | Seccional 1  | LA LIBERTAD AVANZA       | 1162
```

### Valores válidos de Seccional:
- "Seccional 1"
- "Seccional 2"
- ...
- "Seccional 14"

**Importante**: El formato debe ser exactamente `Seccional [número]` (con espacio).

---

## 🔄 Actualizar Datos

Si tienes nuevos archivos Excel con datos actualizados:

1. **Colocar archivos** en la carpeta `data/raw/`:
   ```
   data/raw/2021_porseccional_diputados.xls
   data/raw/2023_porseccional_diputados.xlsx
   data/raw/2025_porseccional_diputados.xlsx
   ```

2. **Ejecutar ETL** para procesar:
   ```bash
   python -m src.etl
   ```

3. **Verificar resultados**:
   - Se crearán archivos en `data/processed/`
   - CSV: `electoral_data_clean.csv`
   - GeoJSON: `seccionales_geo.geojson`
   - Base de datos: `electoral_database.db`

---

## 📱 Usar la Aplicación Web

### Pestañas disponibles:

#### 1. **Maps** (Mapas)
- Mapas coropléticos interactivos
- **Controles**:
  - Año: 2021, 2023, 2025
  - Partido político: Selecciona de la lista
  - Métrica: Porcentaje (%) o Votos totales
- **Visualización**: Mapa de Córdoba con colores por intensidad de voto
- **Tabla**: Ganadores por seccional

#### 2. **Trends** (Tendencias)
- Gráficos de evolución temporal
- **Controles**:
  - Seleccionar múltiples partidos para comparar
- **Visualizaciones**:
  - Línea de tiempo: Evolución de votos
  - Barras: Tasa de crecimiento entre elecciones
  - Distribución por seccional

#### 3. **Analysis** (Análisis Político)
- Métricas politológicas avanzadas
- **Indicadores**:
  - **Índice de Volatilidad** (Pedersen): Mide cambios electorales
  - **Zonas Competitivas**: Seccionales con margen < 5%
  - **Seccionales que cambiaron**: Ganador diferente entre elecciones
  - **HHI**: Concentración electoral
- **Gráficos**:
  - Tabla de seccionales competitivas
  - Gráfico de concentración (HHI)

#### 4. **About** (Acerca de)
- Información del proyecto
- Fuentes de datos
- Tecnologías utilizadas

---

## 🎨 Características

### ✅ Diseño Responsivo
- Funciona en **desktop**, **tablet** y **móvil**
- Se adapta automáticamente al tamaño de pantalla

### ✅ Interactividad
- Gráficos con zoom y hover
- Filtros dinámicos
- Actualizaciones en tiempo real

### ✅ Análisis Político
- Índice de Pedersen (volatilidad electoral)
- Identificación de zonas competitivas
- Análisis de concentración (HHI)

---

## 📁 Estructura de Archivos

```
pyoclaude/
├── app.py                      ← Aplicación web principal
├── setup.bat                   ← Script de instalación
├── run.bat                     ← Script para ejecutar
│
├── data/
│   ├── raw/                    ← Archivos Excel originales (aquí van tus datos)
│   │   ├── 2021_porseccional_diputados.xls
│   │   ├── 2023_porseccional_diputados.xlsx
│   │   └── 2025_porseccional_diputados.xlsx
│   │
│   └── processed/              ← Datos procesados (generados automáticamente)
│       ├── electoral_data_clean.csv
│       ├── seccionales_geo.geojson
│       └── electoral_database.db
│
├── src/
│   ├── etl/                    ← Pipeline de procesamiento
│   ├── analysis/               ← Módulos de análisis
│   └── config/                 ← Configuración
│
└── outputs/                    ← Exportaciones (mapas, reportes)
```

---

## 🔧 Solución de Problemas

### Error: "Module not found"
**Solución**: Activar el entorno virtual y reinstalar dependencias
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "No data available"
**Solución**: Ejecutar el ETL para procesar datos
```bash
python -m src.etl
```

### Error: "Port 8050 already in use"
**Solución**: Cambiar el puerto en `app.py` (línea final):
```python
app.run_server(debug=True, host='0.0.0.0', port=8051)
```

### Los datos no se actualizan
**Solución**: 
1. Verificar que los archivos estén en `data/raw/`
2. Borrar datos procesados: `rm -rf data/processed/*`
3. Ejecutar ETL: `python -m src.etl`
4. Reiniciar la aplicación

---

## 📊 Verificar Datos Procesados

Para verificar que los datos se procesaron correctamente:

```bash
python -c "import pandas as pd; df = pd.read_csv('data/processed/electoral_data_clean.csv'); print(f'Registros: {len(df)}'); print(f'Años: {sorted(df[\"anio\"].unique())}'); print(f'Seccionales: {len(df[\"seccional\"].unique())}'); print(f'Partidos: {len(df[\"agrupacion\"].unique())}')"
```

**Resultado esperado**:
```
Registros: 420
Años: [2021, 2023, 2025]
Seccionales: 14
Partidos: 24
```

---

## 📚 Documentación Adicional

- **QUICK_START.md**: Guía rápida de inicio
- **CLAUDE.md**: Documentación técnica completa
- **PLAN_PROYECTO.md**: Arquitectura y diseño del sistema
- **UPDATE_NOTES.md**: Cambios en formato de datos
- **IMPLEMENTATION_SUMMARY.md**: Resumen de implementación

---

## 💡 Consejos

1. **Actualizar datos**: Siempre coloca los archivos nuevos en `data/raw/` y ejecuta el ETL
2. **Personalizar colores**: Edita `data/mappings/party_colors.json`
3. **Exportar datos**: Los datos procesados están en CSV y SQLite para análisis externos
4. **Responsive**: Prueba la aplicación en diferentes dispositivos

---

## ✅ Todo Listo

El sistema está completamente funcional. Para comenzar:

```cmd
run.bat
```

Luego abre tu navegador en `http://127.0.0.1:8050` y explora los datos electorales!

🗳️ **¡Disfruta tu análisis electoral!** 📊
