# MCP Server para Análisis de UI/UX del Dashboard Electoral

## Descripción

Este MCP (Model Context Protocol) Server proporciona herramientas automatizadas para analizar y mejorar el diseño, responsividad, accesibilidad y usabilidad del Dashboard Electoral de Córdoba Capital.

El servidor implementa principios de diseño moderno **context-aware** (consciente del contexto) siguiendo las mejores prácticas de UI/UX de 2025.

---

## Características

### Herramientas Disponibles

1. **analyze_responsive_design** - Analiza patrones de diseño responsivo usando Bootstrap
2. **validate_party_colors** - Valida que los colores de partidos políticos coincidan con el sistema de diseño
3. **check_accessibility** - Verifica cumplimiento WCAG 2.1 AA
4. **suggest_ui_improvements** - Sugiere mejoras de UI/UX modernas
5. **get_design_recommendations** - Obtiene recomendaciones específicas por categoría

### Recursos Disponibles

- `design://system` - Sistema de diseño completo
- `design://party-colors` - Paleta de colores de partidos políticos
- `design://responsive-breakpoints` - Breakpoints responsivos de Bootstrap
- `design://accessibility-rules` - Reglas de accesibilidad WCAG 2.1 AA

---

## Instalación

### 1. Instalar Dependencias

```bash
pip install mcp
```

### 2. Estructura de Archivos

```
src/mcp_server/
├── server.py                    # Servidor MCP principal
├── config/
│   └── design_system.json       # Configuración del sistema de diseño
└── tools/                       # (futuras herramientas adicionales)
```

---

## Uso

### Opción 1: Análisis Automatizado (Recomendado)

Ejecutar el script de análisis completo:

```bash
python analyze_dashboard.py
```

Esto generará:
- **Reporte en consola** con análisis completo
- **JSON detallado**: `outputs/analysis/dashboard_ui_analysis.json`
- **Archivo de texto**: `dashboard_analysis_report.txt`

### Opción 2: Usar el Servidor MCP Directamente

#### A. Iniciar el Servidor

```bash
python -m src.mcp_server.server
```

#### B. Configurar en Claude Code

```bash
# Windows
claude mcp add --transport stdio dash-designer --scope project -- \
  cmd /c "python -m src.mcp_server.server"

# Linux/Mac
claude mcp add --transport stdio dash-designer --scope project -- \
  python -m src.mcp_server.server
```

#### C. Verificar Instalación

```bash
claude mcp list
claude mcp get dash-designer
```

#### D. Usar en Claude Code

```
Use the dash-designer MCP server to:
1. Analyze app.py for responsive design
2. Validate party colors
3. Check WCAG accessibility
4. Suggest UI improvements
```

---

## Resultados del Último Análisis

### Resumen Ejecutivo

| Aspecto | Puntuación | Estado |
|---------|------------|--------|
| **Diseño Responsivo** | 90/100 | ✅ Excellent |
| **Colores Partidos** | 100% | ✅ Válido |
| **Accesibilidad** | 65/100 | ⚠️ Partial AA |
| **Total Sugerencias** | 4 | 📋 Identificadas |

### Prioridades Inmediatas

1. **[HIGH]** Actualizar `go.Choroplethmapbox` → `go.Choroplethmap` (deprecated en Plotly)
2. **[HIGH]** Actualizar `go.Scattermapbox` → `go.Scattermap` (deprecated en Plotly)
3. **[MEDIUM]** Agregar ARIA labels a gráficos interactivos para accesibilidad
4. **[MEDIUM]** Revisar jerarquía de headings (H1 → H5, falta H2-H4)
5. **[LOW]** Considerar diseño responsivo para xs/sm breakpoints (móviles)

---

## Sistema de Diseño

### Colores de Partidos Políticos

```json
{
  "LA LIBERTAD AVANZA": "#9370DB",           // Violeta
  "JUNTOS POR EL CAMBIO": "#FFD700",         // Amarillo
  "HACEMOS POR CÓRDOBA": "#87CEEB",          // Celeste
  "UNIÓN POR LA PATRIA": "#0047AB",          // Azul
  "FRENTE DE IZQUIERDA": "#DC143C"           // Rojo
}
```

### Breakpoints Responsivos (Bootstrap)

- **xs**: 0-575px (móviles portrait)
- **sm**: 576-767px (móviles landscape)
- **md**: 768-991px (tablets)
- **lg**: 992-1199px (desktops)
- **xl**: 1200-1399px (desktops grandes)
- **xxl**: 1400px+ (monitores ultra anchos)

### Reglas de Accesibilidad

- Contraste mínimo: **4.5:1** (texto normal)
- Tamaño táctil mínimo: **44x44px**
- ARIA labels: **Requeridos** para elementos interactivos
- Navegación por teclado: **Obligatoria**
- Compatibilidad con lectores de pantalla: **Obligatoria**

---

## Ejemplo de Uso Programático

```python
import asyncio
from src.mcp_server.server import (
    analyze_responsive_design,
    validate_party_colors,
    check_accessibility
)

async def analyze_dashboard():
    # Leer código del dashboard
    with open('app.py', 'r') as f:
        code = f.read()

    # Analizar diseño responsivo
    responsive = await analyze_responsive_design(code)
    print(responsive[0].text)

    # Validar colores
    colors = await validate_party_colors(code)
    print(colors[0].text)

    # Verificar accesibilidad
    accessibility = await check_accessibility(code)
    print(accessibility[0].text)

asyncio.run(analyze_dashboard())
```

---

## Mejoras Recomendadas para el Dashboard

### 1. Actualizar APIs Deprecated de Plotly

**Antes:**
```python
fig_map.add_trace(go.Choroplethmapbox(
    geojson=geojson,
    marker_opacity=0.6
))

fig_map.add_trace(go.Scattermapbox(
    lat=gdf_year['lat'],
    lon=gdf_year['lon']
))
```

**Después:**
```python
fig_map.add_trace(go.Choroplethmap(
    geojson=geojson,
    marker_opacity=0.6
))

fig_map.add_trace(go.Scattermap(
    lat=gdf_year['lat'],
    lon=gdf_year['lon']
))
```

**Referencia:** https://plotly.com/python/mapbox-to-maplibre/

### 2. Mejorar Accesibilidad con ARIA Labels

**Antes:**
```python
dcc.Graph(id="electoral-map", style={"height": "600px"})
```

**Después:**
```python
dcc.Graph(
    id="electoral-map",
    style={"height": "600px"},
    config={'displayModeBar': True},
    aria={'label': 'Mapa electoral interactivo de Córdoba Capital'}
)
```

### 3. Corregir Jerarquía de Headings

**Antes:**
```python
html.H1("Dashboard Electoral Córdoba Capital"),
html.H5("Evolución 2021 - 2023 - 2025"),
html.H5("Mapa Electoral por Seccional")
```

**Después:**
```python
html.H1("Dashboard Electoral Córdoba Capital"),
html.H2("Evolución 2021 - 2023 - 2025"),
html.H3("Mapa Electoral por Seccional")
```

### 4. Usar Unidades Relativas para Heights

**Antes:**
```python
style={"height": "600px"}
style={"height": "280px"}
style={"height": "450px"}
```

**Después:**
```python
style={"height": "60vh"}
style={"height": "28vh"}
style={"height": "45vh"}
```

### 5. Agregar Responsive Breakpoints para Móviles

**Antes:**
```python
dbc.Col([...], md=3)
dbc.Col([...], md=8)
```

**Después:**
```python
dbc.Col([...], xs=12, sm=6, md=3)
dbc.Col([...], xs=12, sm=12, md=8, lg=9)
```

---

## Arquitectura del MCP Server

### Componentes Principales

```
┌─────────────────────────────────────────┐
│         Claude Code / AI Client         │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
                 │ (stdio/HTTP)
                 │
┌────────────────▼────────────────────────┐
│       MCP Server (server.py)            │
│  ┌──────────────────────────────────┐   │
│  │  Tools (5 herramientas)          │   │
│  ├──────────────────────────────────┤   │
│  │  Resources (4 recursos)          │   │
│  ├──────────────────────────────────┤   │
│  │  Design System Config (JSON)     │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                 │
                 │ Análisis
                 │
┌────────────────▼────────────────────────┐
│       Dashboard Code (app.py)           │
│  ┌──────────────────────────────────┐   │
│  │  Layout (HTML/Dash)              │   │
│  │  Callbacks (Interactividad)      │   │
│  │  Visualizaciones (Plotly)        │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Flujo de Análisis

1. **Lectura**: MCP server lee `app.py`
2. **Análisis**: Ejecuta herramientas de análisis
   - Responsive design patterns
   - Color validation
   - Accessibility checks
   - UI/UX suggestions
3. **Reporte**: Genera JSON + texto con recomendaciones
4. **Acción**: Usuario implementa mejoras sugeridas

---

## Configuración del Sistema de Diseño

Editar `src/mcp_server/config/design_system.json` para personalizar:

- **party_colors**: Agregar/modificar colores de partidos
- **responsive_breakpoints**: Ajustar breakpoints
- **accessibility_rules**: Configurar reglas WCAG
- **ui_best_practices**: Definir escalas de tipografía, spacing, etc.
- **dashboard_specific**: Estilos específicos para mapas, charts, cards

---

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'mcp'`

**Solución:**
```bash
pip install mcp
```

### Error: `UnicodeEncodeError` en consola Windows

**Solución:**
Redirigir output a archivo:
```bash
python analyze_dashboard.py > report.txt 2>&1
```

### Error: Conflictos de dependencias con FastAPI/Pydantic

**Solución:**
```bash
# Crear virtual environment aislado
python -m venv venv_mcp
venv_mcp\Scripts\activate
pip install mcp
python -m src.mcp_server.server
```

### MCP Server no aparece en Claude Code

**Solución:**
1. Verificar instalación: `claude mcp list`
2. Reiniciar Claude Code
3. Verificar logs: `claude mcp get dash-designer --verbose`

---

## Próximas Mejoras

- [ ] Implementar análisis de performance (Lighthouse score)
- [ ] Agregar validación de contraste de colores automática
- [ ] Integrar con herramientas de testing (Playwright, Cypress)
- [ ] Exportar reporte en PDF/HTML con gráficos
- [ ] Implementar modo "auto-fix" para correcciones automáticas
- [ ] Agregar soporte para análisis de múltiples páginas/dashboards

---

## Referencias

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Code MCP Guide](https://code.claude.com/docs/en/mcp.md)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Plotly MapLibre Migration](https://plotly.com/python/mapbox-to-maplibre/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)

---

## Licencia

Proyecto educativo - Libre uso

---

## Contacto

Para preguntas o mejoras, consultar documentación en:
- `CLAUDE.md` - Instrucciones del proyecto
- `PLAN_PROYECTO.md` - Plan de implementación

**Última actualización:** 2025-12-25
**Versión MCP Server:** 1.0.0
**Compatible con:** Python 3.10+
