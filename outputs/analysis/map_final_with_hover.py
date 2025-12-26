"""
Mapa electoral con efecto hover de resaltado
- Estilo balanced (bordes 1.5px)
- Hover effect como Folium
"""
import geopandas as gpd
import plotly.graph_objects as go
import folium
from folium import DivIcon
import json

print("="*70)
print("GENERANDO MAPAS CON EFECTO HOVER DE RESALTADO")
print("="*70)

# Cargar y preparar datos
print("\n1. Cargando GeoJSON...")
gdf = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf['geometry'] = gdf.geometry.buffer(0)
dissolved = gdf.dissolve(by='Seccional').reset_index()
dissolved['geometry'] = dissolved.geometry.simplify(tolerance=0.001, preserve_topology=True)
dissolved['nombre'] = dissolved['Seccional'].apply(lambda x: f'Seccional {x}')
dissolved['seccional_num'] = dissolved['Seccional'].astype(int)
dissolved = dissolved.sort_values('seccional_num')

# Centroides
dissolved['centroid'] = dissolved.geometry.centroid
dissolved['lat'] = dissolved['centroid'].y
dissolved['lon'] = dissolved['centroid'].x

print(f"   OK - {len(dissolved)} seccionales procesados")

# ============================================================================
# VERSIÓN 1: FOLIUM CON ESTILO BALANCED Y HOVER NATIVO
# ============================================================================
print("\n2. Creando versión Folium con hover (RECOMENDADO)...")

m = folium.Map(
    location=[-31.4201, -64.1888],
    zoom_start=12,
    tiles='CartoDB positron',
    max_zoom=14,
    min_zoom=11
)

# Estilo base (estado normal)
style_function = lambda x: {
    'fillColor': '#87CEEB',
    'fillOpacity': 0.45,
    'color': '#4a4a4a',  # Gris oscuro elegante (igual que balanced)
    'weight': 1.5,       # 1.5px como balanced
    'opacity': 1
}

# Estilo hover (cuando pasas el mouse)
highlight_function = lambda x: {
    'fillColor': '#87CEEB',
    'fillOpacity': 0.75,  # Más opaco al hover
    'color': '#FF6B6B',   # Rojo coral elegante (no tan fuerte)
    'weight': 3,          # Borde más grueso al hover
    'opacity': 1
}

# GeoJSON limpio
gdf_for_map = dissolved[['Seccional', 'nombre', 'geometry']].copy()

# Agregar polígonos con hover
folium.GeoJson(
    gdf_for_map,
    name='Seccionales',
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['nombre'],
        aliases=[''],
        style=(
            "background-color: white; "
            "color: #333333; "
            "font-family: Arial, sans-serif; "
            "font-size: 14px; "
            "font-weight: bold; "
            "padding: 10px; "
            "border: 2px solid #4a4a4a; "
            "border-radius: 4px; "
            "box-shadow: 0 2px 4px rgba(0,0,0,0.2);"
        ),
        sticky=False
    )
).add_to(m)

# Etiquetas permanentes
for idx, row in dissolved.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=DivIcon(html=f"""
            <div style="
                font-family: Arial, sans-serif;
                font-size: 13px;
                font-weight: 500;
                color: #1a1a1a;
                text-align: center;
                text-shadow:
                    -1px -1px 0 #FFF,
                    1px -1px 0 #FFF,
                    -1px 1px 0 #FFF,
                    1px 1px 0 #FFF,
                    0 0 3px #FFF;
                pointer-events: none;
            ">
                {row['nombre']}
            </div>
        """)
    ).add_to(m)

m.save('outputs/analysis/map_final_folium_hover.html')
print("   OK - Guardado: map_final_folium_hover.html")

# ============================================================================
# VERSIÓN 2: PLOTLY CON HOVER MEJORADO (tooltip más visible)
# ============================================================================
print("\n3. Creando versión Plotly con hover mejorado...")

geojson = json.loads(gdf_for_map.to_json())

fig = go.Figure()

# Polígonos
fig.add_trace(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf_for_map.index,
    z=[1]*len(gdf_for_map),
    colorscale=[[0, '#87CEEB'], [1, '#87CEEB']],
    showscale=False,
    marker_opacity=0.45,
    marker_line_width=1.5,
    marker_line_color='#4a4a4a',
    hovertemplate=(
        '<b style="font-size:16px;">%{text}</b><br>'
        '<i>Click para más información</i>'
        '<extra></extra>'
    ),
    text=gdf_for_map['nombre'],
    name='Seccionales'
))

# Etiquetas
fig.add_trace(go.Scattermapbox(
    lat=dissolved['lat'],
    lon=dissolved['lon'],
    mode='text',
    text=dissolved['nombre'],
    textfont=dict(
        size=13,
        color='#1a1a1a',
        family='Arial, sans-serif'
    ),
    textposition='middle center',
    hoverinfo='skip',
    showlegend=False
))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=11.8,
    mapbox_center={"lat": -31.4201, "lon": -64.1888},
    margin={"r":0, "t":60, "l":0, "b":0},
    title={
        'text': 'Seccionales Electorales - Córdoba Capital',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18, 'family': 'Arial', 'color': '#333'}
    },
    height=700,
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial",
        font_color="#333",
        bordercolor="#4a4a4a",
        align="left"
    )
)

fig.write_html('outputs/analysis/map_final_plotly_hover.html')
print("   OK - Guardado: map_final_plotly_hover.html")

# ============================================================================
# VERSIÓN 3: FOLIUM CON HOVER MÁS SUTIL (alternativa)
# ============================================================================
print("\n4. Creando versión con hover sutil...")

m_subtle = folium.Map(
    location=[-31.4201, -64.1888],
    zoom_start=12,
    tiles='CartoDB positron',
    max_zoom=14,
    min_zoom=11
)

# Estilo hover más sutil
highlight_subtle = lambda x: {
    'fillColor': '#5DADE2',  # Celeste más intenso
    'fillOpacity': 0.65,
    'color': '#2E86AB',      # Azul elegante
    'weight': 2.5,
    'opacity': 1
}

folium.GeoJson(
    gdf_for_map,
    name='Seccionales',
    style_function=style_function,
    highlight_function=highlight_subtle,
    tooltip=folium.GeoJsonTooltip(
        fields=['nombre'],
        aliases=[''],
        style=(
            "background-color: white; "
            "color: #333333; "
            "font-family: Arial, sans-serif; "
            "font-size: 14px; "
            "font-weight: bold; "
            "padding: 10px; "
            "border: 2px solid #2E86AB; "
            "border-radius: 4px; "
            "box-shadow: 0 2px 4px rgba(0,0,0,0.2);"
        ),
        sticky=False
    )
).add_to(m_subtle)

for idx, row in dissolved.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=DivIcon(html=f"""
            <div style="
                font-family: Arial, sans-serif;
                font-size: 13px;
                font-weight: 500;
                color: #1a1a1a;
                text-align: center;
                text-shadow:
                    -1px -1px 0 #FFF,
                    1px -1px 0 #FFF,
                    -1px 1px 0 #FFF,
                    1px 1px 0 #FFF,
                    0 0 3px #FFF;
                pointer-events: none;
            ">
                {row['nombre']}
            </div>
        """)
    ).add_to(m_subtle)

m_subtle.save('outputs/analysis/map_final_hover_subtle.html')
print("   OK - Guardado: map_final_hover_subtle.html")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*70)
print("MAPAS CON HOVER GENERADOS")
print("="*70)
print("\nSe crearon 3 versiones:")
print("\n1. map_final_folium_hover.html ⭐ RECOMENDADO")
print("   - Folium con estilo balanced (bordes 1.5px)")
print("   - Hover: borde rojo coral + más opaco")
print("   - Efecto nativo de Folium (funciona perfectamente)")
print("\n2. map_final_plotly_hover.html")
print("   - Plotly con estilo balanced")
print("   - Hover: tooltip mejorado (sin resaltado visual del polígono)")
print("   - Nota: Plotly no soporta highlight visual nativamente")
print("\n3. map_final_hover_subtle.html")
print("   - Folium con hover más sutil (azul)")
print("   - Alternativa si el rojo coral es muy fuerte")
print("\nEfecto hover en cada versión:")
print("  Folium #1: Borde rojo coral (3px) + opacidad 75%")
print("  Plotly #2: Solo tooltip visible (sin resaltado de polígono)")
print("  Folium #3: Borde azul elegante (2.5px) + celeste intenso")
print("\n¡Abre map_final_folium_hover.html para ver el efecto completo!")
print()
