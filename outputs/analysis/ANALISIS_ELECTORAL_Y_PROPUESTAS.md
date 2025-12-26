# Análisis Electoral Córdoba Capital 2021-2025
## Propuestas de Visualización Profesional

**Fecha:** 2025-12-25
**Fuente de datos:** Electoral data clean (420 registros, 14 seccionales, 3 años)

---

## 📊 HALLAZGOS CLAVE

### Evolución Electoral por Año

**2021 - DOMINACIÓN AMARILLA**
- **JUNTOS POR EL CAMBIO**: 14/14 seccionales (100%)
- Mapa completamente amarillo
- Rangos: 49.41% (Seccional 5) a 61.13% (Seccional 9)

**2023 - MAPA FRAGMENTADO**
- **LA LIBERTAD AVANZA**: 8/14 seccionales (57%)
  - Seccionales: 2, 7, 8, 10, 11, 12, 13, 14
- **JUNTOS POR EL CAMBIO**: 4/14 seccionales (29%)
  - Seccionales: 1, 3, 4, 9
- **HACEMOS POR CÓRDOBA**: 2/14 seccionales (14%)
  - Seccionales: 5, 6

**2025 - DOMINACIÓN VIOLETA**
- **ALIANZA LA LIBERTAD AVANZA**: 13/14 seccionales (93%)
  - Todas excepto la Seccional 5 (dato faltante)
- Mapa casi completamente violeta
- Rangos: 32.43% (Seccional 1) a 49.64% (Seccional 4)

---

## 🎨 PALETA DE COLORES ELECTORAL

Basado en convenciones argentinas y análisis de referentes (La Nación, Perfil, Página12):

### Colores Principales

```python
PARTY_COLORS = {
    # Principales fuerzas
    'LA LIBERTAD AVANZA': '#9370DB',           # Violeta (color oficial LLA)
    'ALIANZA LA LIBERTAD AVANZA': '#9370DB',   # Mismo violeta
    'JUNTOS POR EL CAMBIO': '#FFD700',         # Amarillo (color oficial JxC)
    'HACEMOS POR CÓRDOBA': '#87CEEB',          # Celeste (cordobesismo)
    'UNIÓN POR LA PATRIA': '#0047AB',          # Azul (peronismo)

    # Fuerzas menores
    'FRENTE DE IZQUIERDA': '#DC143C',                      # Rojo
    'FRENTE DE IZQUIERDA  Y DE TRABAJADORES - UNIDAD': '#DC143C',
    'ENCUENTRO VECINAL CÓRDOBA': '#98D8C8',                # Verde agua
    'ALIANZA PROVINCIAS UNIDAS': '#F08080',                # Coral
    'DEFENDAMOS CÓRDOBA': '#20B2AA',                       # Verde azulado

    # Default para otros
    'DEFAULT': '#CCCCCC'  # Gris para partidos sin definir
}
```

### Paleta de Intensidad (por margen de victoria)

```python
INTENSITY_RANGES = {
    'landslide': (50, 100),   # Victoria aplastante → color intenso
    'strong': (40, 50),       # Victoria sólida → color estándar
    'moderate': (30, 40),     # Victoria moderada → color más claro
    'tight': (0, 30)          # Victoria ajustada → color muy claro + borde especial
}
```

---

## 🌐 REFERENCIAS Y BENCHMARKS

### Medios Argentinos

**La Nación - Elecciones Córdoba 2023**
- URL: https://www.lanacion.com.ar/politica/elecciones-en-cordoba-el-mapa-de-los-resultados-en-tiempo-real-distrito-por-distrito-nid25062023/
- Estilo: Mapa coroplético con colores por partido ganador
- Interactividad: Click en departamento → datos detallados
- Paleta: Colores institucionales de partidos
- Leyenda: Clara, con porcentajes

**Perfil - "Así se pintó de violeta Córdoba 2025"**
- URL: https://www.perfil.com/noticias/cordoba/asi-se-pinto-de-violeta-la-provincia-de-cordoba-en-las-elecciones-legislativas-2025.phtml
- Enfoque: Narrativa visual del cambio electoral
- Título menciona "violeta" → referencia al color de LLA

**Página12 - Mapa interactivo Córdoba 2023**
- URL: https://www.pagina12.com.ar/562215-elecciones-cordoba-2023-el-mapa-interactivo-con-los-resultad
- Distrito por distrito
- Comparativa histórica

### Proyectos GitHub

**1. electorArg/PolAr_Data**
- URL: https://github.com/electorArg/PolAr_Data
- Datos electorales argentinos desde 2007
- Shapefiles de provincias y departamentos
- Layouts geofacet para Argentina y 24 provincias
- **MUY ÚTIL:** Podrías contribuir tu análisis de Córdoba aquí

**2. matuteiglesias/elecciones-ARG**
- URL: https://github.com/matuteiglesias/elecciones-ARG
- Análisis elecciones 2025 con Mapbox
- Notebooks + estilos web
- Foco en Buenos Aires y distritos
- **INSPIRACIÓN:** Estilo moderno con DuckDB/Parquet

**3. tartagalensis/circuitos_electorales_AR**
- URL: https://github.com/tartagalensis/circuitos_electorales_AR
- GeoJSON de circuitos electorales de toda Argentina
- Formato: Circuit, Codprov, Coddepto, Geometry
- **SIMILAR A TU CASO:** Podrías contrastar tus GeoJSON

**4. PoliticaArgentina/data_warehouse**
- URL: https://github.com/PoliticaArgentina/data_warehouse
- Resultados electorales 2003-2019
- Datos a nivel mesa electoral
- **CONTEXTO HISTÓRICO** para comparar tendencias

---

## 🎯 PROPUESTAS DE VISUALIZACIÓN

### PROPUESTA 1: Mapas Estáticos Lado a Lado ⭐ SIMPLE

**Descripción:** Tres mapas (2021, 2023, 2025) uno al lado del otro

**Layout:**
```
┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│  ELECCIONES  │  ELECCIONES  │  ELECCIONES  │
│     2021     │     2023     │     2025     │
│              │              │              │
│  [AMARILLO]  │ [MULTICOLOR] │  [VIOLETA]   │
│              │              │              │
└──────────────┴──────────────┴──────────────┘
```

**Ventajas:**
- ✅ Fácil de implementar
- ✅ Comparación visual instantánea
- ✅ Perfecto para informes estáticos
- ✅ Exportable a PNG/PDF

**Desventajas:**
- ⚠️ No interactivo
- ⚠️ Ocupa mucho espacio horizontal

**Implementación:** Plotly subplots o Matplotlib

**Código base:**
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2021', '2023', '2025'),
    specs=[[{'type': 'scattermapbox'}] * 3]
)

# Agregar mapa para cada año...
```

---

### PROPUESTA 2: Slider Temporal Interactivo ⭐⭐ RECOMENDADO

**Descripción:** Un solo mapa con slider para navegar entre años

**Layout:**
```
┌─────────────────────────────────────────┐
│                                         │
│        EVOLUCIÓN ELECTORAL              │
│      CÓRDOBA CAPITAL 2021-2025          │
│                                         │
│    [MAPA INTERACTIVO CON COLORES]       │
│                                         │
│                                         │
│  ◄─────●─────────────────────────► │
│       2021    2023    2025              │
│                                         │
│  LEYENDA:                               │
│  ■ La Libertad Avanza  ■ JxC  ■ HxC     │
└─────────────────────────────────────────┘
```

**Ventajas:**
- ✅ Interactivo y moderno
- ✅ Ahorra espacio
- ✅ Muestra transición temporal
- ✅ Animación automática opcional
- ✅ Perfecto para dashboards web

**Desventajas:**
- ⚠️ Más complejo de implementar
- ⚠️ Requiere JavaScript/Plotly

**Implementación:** Plotly con `frames` y `sliders`

**Código base:**
```python
import plotly.graph_objects as go

# Crear frames para cada año
frames = []
for year in [2021, 2023, 2025]:
    frame_data = create_choropleth_for_year(year)
    frames.append(go.Frame(data=[frame_data], name=str(year)))

# Configurar slider
sliders = [dict(
    active=0,
    steps=[dict(
        label=str(year),
        method="animate",
        args=[[str(year)]]
    ) for year in [2021, 2023, 2025]]
)]

fig = go.Figure(data=frames[0].data, frames=frames)
fig.update_layout(sliders=sliders)
```

---

### PROPUESTA 3: Dashboard Comparativo con Métricas ⭐⭐⭐ PROFESIONAL

**Descripción:** Dashboard completo con mapas + gráficos + métricas

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  ELECCIONES CÓRDOBA CAPITAL 2021-2025               │
├────────────────────┬────────────────────────────────┤
│                    │  MÉTRICAS CLAVE                │
│                    │  ┌──────┬──────┬──────┐        │
│                    │  │ 2021 │ 2023 │ 2025 │        │
│   MAPA PRINCIPAL   │  ├──────┼──────┼──────┤        │
│   (con slider)     │  │ 760k │ 785k │ 820k │ Votos │
│                    │  │  72% │  68% │  64% │ Part. │
│                    │  └──────┴──────┴──────┘        │
├────────────────────┴────────────────────────────────┤
│  EVOLUCIÓN POR PARTIDO                              │
│  ╔════════════════════════════════════════╗         │
│  ║  [Gráfico de líneas: votos por año]   ║         │
│  ╚════════════════════════════════════════╝         │
├─────────────────────────────────────────────────────┤
│  MAPA DE CAMBIO (SWING)                             │
│  ┌──────────────┬──────────────┐                    │
│  │  2021 → 2023 │  2023 → 2025 │                    │
│  │  [Mapa Δ%]   │  [Mapa Δ%]   │                    │
│  └──────────────┴──────────────┘                    │
└─────────────────────────────────────────────────────┘
```

**Componentes:**
1. **Mapa principal:** Con slider temporal
2. **Métricas:** Total votos, participación, etc.
3. **Gráfico de evolución:** Líneas por partido
4. **Mapas de cambio:** Diferencia porcentual entre períodos

**Ventajas:**
- ✅ Vista completa del panorama electoral
- ✅ Análisis profundo con contexto
- ✅ Ideal para presentaciones ejecutivas
- ✅ Reutilizable para futuros análisis

**Desventajas:**
- ⚠️ Requiere más desarrollo
- ⚠️ Necesita Dash o Streamlit

**Implementación:** Dash (Plotly) o Streamlit

---

### PROPUESTA 4: Mapa de Swing/Cambio Electoral ⭐⭐ ANALÍTICO

**Descripción:** Visualizar el CAMBIO entre elecciones, no solo el ganador

**Concepto:**
- Mapa 1: Cambio 2021 → 2023
- Mapa 2: Cambio 2023 → 2025

**Colores por cambio:**
```
Ganó LLA desde JxC:      Violeta → Violeta más intenso
Ganó LLA desde HxC:      Celeste → Violeta
Mantuvo JxC:             Amarillo → Amarillo
Cambió de JxC a HxC:     Amarillo → Celeste
etc.
```

**O con gradiente de swing:**
```
Swing +20% hacia LLA:    Violeta intenso
Swing +10% hacia LLA:    Violeta medio
Sin cambio significativo: Gris
Swing -10% desde LLA:    Color opositor claro
```

**Ventajas:**
- ✅ Muestra DINÁMICA electoral, no solo resultado
- ✅ Identifica patrones de migración de votos
- ✅ Útil para análisis politológico

**Desventajas:**
- ⚠️ Requiere cálculos adicionales
- ⚠️ Puede ser confuso para público general

---

### PROPUESTA 5: Animación Temporal con Transiciones ⭐⭐⭐ IMPACTANTE

**Descripción:** GIF o video mostrando el mapa cambiando de color año a año

**Concepto:**
1. Mapa 2021 (todo amarillo) → pausa 2s
2. Transición gradual a 2023 (colores cambian) → pausa 2s
3. Transición gradual a 2025 (todo violeta) → pausa 2s
4. Loop o detener

**Efectos:**
- Fade entre colores
- Animación de números (contador de votos)
- Highlight de seccionales que cambian

**Ventajas:**
- ✅ MUY IMPACTANTE visualmente
- ✅ Perfecto para redes sociales
- ✅ Cuenta una "historia" electoral
- ✅ Exportable como GIF/MP4

**Desventajas:**
- ⚠️ No permite interacción (en GIF)
- ⚠️ Requiere librerías de animación

**Implementación:** Plotly animations, Matplotlib animation, o Manim

---

### PROPUESTA 6: Mapas Pequeños Múltiples (Small Multiples) ⭐ COMPACTO

**Descripción:** Grilla de mapas pequeños para comparar múltiples dimensiones

**Layout:**
```
┌─────────┬─────────┬─────────┐
│  2021   │  2023   │  2025   │
│ Ganador │ Ganador │ Ganador │
├─────────┼─────────┼─────────┤
│  2021   │  2023   │  2025   │
│   LLA   │   LLA   │   LLA   │
├─────────┼─────────┼─────────┤
│  2021   │  2023   │  2025   │
│   JxC   │   JxC   │   JxC   │
└─────────┴─────────┴─────────┘
```

**Cada fila:**
- Fila 1: Ganador por seccional
- Fila 2: % de votos de LLA
- Fila 3: % de votos de JxC

**Ventajas:**
- ✅ Múltiples vistas en poco espacio
- ✅ Comparación detallada por partido
- ✅ Ideal para informes técnicos

**Desventajas:**
- ⚠️ Mapas muy pequeños (difícil leer etiquetas)
- ⚠️ Sobrecarga visual si hay muchos

---

## 🏆 MI RECOMENDACIÓN FINAL

### Para tu proyecto, recomiendo COMBINAR:

**1. Propuesta 2 (Slider Temporal) como vista principal**
- Dashboard web con mapa interactivo
- Slider para navegar 2021 → 2023 → 2025
- Hover para ver datos detallados por seccional
- Botón "Play" para animación automática

**2. Propuesta 1 (Mapas lado a lado) para reportes**
- Exportar imagen PNG de alta resolución
- 3 mapas en fila
- Incluir en documentos PDF/PPT

**3. Propuesta 4 (Mapas de swing) como análisis adicional**
- Sección "Análisis de cambio electoral"
- 2 mapas mostrando swing 2021→2023 y 2023→2025

---

## 📝 ROADMAP DE IMPLEMENTACIÓN

### Fase 1: Mapas Básicos con Colores (AHORA) ⭐
**Objetivo:** Generar los 3 mapas (2021, 2023, 2025) con colores por partido ganador

**Tareas:**
1. ✅ Definir paleta de colores (HECHO arriba)
2. Crear función `get_winner_color(seccional, year)`
3. Generar 3 mapas HTML individuales
4. Probar con estilo `map_final_hover_subtle.html`

**Tiempo estimado:** 1-2 horas

---

### Fase 2: Dashboard con Slider (SIGUIENTE)
**Objetivo:** Mapa interactivo con slider temporal

**Tareas:**
1. Convertir mapas a Plotly frames
2. Configurar slider con años
3. Agregar animación automática
4. Agregar leyenda dinámica
5. Deploy en Streamlit o Dash

**Tiempo estimado:** 3-4 horas

---

### Fase 3: Análisis Avanzado (OPCIONAL)
**Objetivo:** Mapas de swing y dashboard completo

**Tareas:**
1. Calcular cambios porcentuales entre períodos
2. Generar mapas de swing
3. Crear gráficos de evolución temporal
4. Integrar en dashboard completo
5. Documentar y publicar en GitHub

**Tiempo estimado:** 6-8 horas

---

## 🎨 CÓDIGO PARA EMPEZAR AHORA

Te creo una función que genera los mapas con colores por partido ganador usando el estilo `map_final_hover_subtle.html` que te encantó.

**¿Procedo con la implementación de la Fase 1?**

Generaría:
- `map_electoral_2021.html`
- `map_electoral_2023.html`
- `map_electoral_2025.html`

Cada uno con:
- ✅ Colores por partido ganador
- ✅ Estilo elegante (bordes suaves azules)
- ✅ Hover effect sutil
- ✅ Etiquetas "Seccional X"
- ✅ Tooltip con datos: partido, votos, porcentaje

**¿Te parece bien?** Dime y arranco con el código.

---

## 📚 SOURCES

- [La Nación - Elecciones Córdoba 2023](https://www.lanacion.com.ar/politica/elecciones-en-cordoba-el-mapa-de-los-resultados-en-tiempo-real-distrito-por-distrito-nid25062023/)
- [Perfil - Córdoba se pintó de violeta 2025](https://www.perfil.com/noticias/cordoba/asi-se-pinto-de-violeta-la-provincia-de-cordoba-en-las-elecciones-legislativas-2025.phtml)
- [Página12 - Mapa interactivo Córdoba 2023](https://www.pagina12.com.ar/562215-elecciones-cordoba-2023-el-mapa-interactivo-con-los-resultad)
- [GitHub: electorArg/PolAr_Data](https://github.com/electorArg/PolAr_Data)
- [GitHub: matuteiglesias/elecciones-ARG](https://github.com/matuteiglesias/elecciones-ARG)
- [GitHub: tartagalensis/circuitos_electorales_AR](https://github.com/tartagalensis/circuitos_electorales_AR)
- [GitHub: PoliticaArgentina/data_warehouse](https://github.com/PoliticaArgentina/data_warehouse)
