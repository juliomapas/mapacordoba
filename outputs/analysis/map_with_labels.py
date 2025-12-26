"""
Mapas con etiquetas visibles y bordes claros
Compara Folium vs Plotly para visualización profesional
"""
import geopandas as gpd
import folium
from folium import DivIcon
import plotly.graph_objects as go
import json

print("="*70)
print("GENERANDO MAPAS CON ETIQUETAS VISIBLES")
print("="*70)

# Cargar y preparar datos
print("\n1. Cargando GeoJSON...")
gdf = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf['geometry'] = gdf.geometry.buffer(0)  # Reparar
dissolved = gdf.dissolve(by='Seccional').reset_index()
dissolved['geometry'] = dissolved.geometry.simplify(tolerance=0.001, preserve_topology=True)
dissolved['nombre'] = dissolved['Seccional'].apply(lambda x: f'Seccional {x}')
dissolved['seccional_num'] = dissolved['Seccional'].astype(int)
dissolved = dissolved.sort_values('seccional_num')

# Calcular centroides para etiquetas
dissolved['centroid'] = dissolved.geometry.centroid
dissolved['lat'] = dissolved['centroid'].y
dissolved['lon'] = dissolved['centroid'].x

print(f"   OK - {len(dissolved)} seccionales procesados")

# ============================================================================
# OPCIÓN 1: FOLIUM CON ETIQUETAS PERMANENTES
# ============================================================================
print("\n2. Creando mapa Folium con etiquetas permanentes...")

m_folium = folium.Map(
    location=[-31.4201, -64.1888],
    zoom_start=12,
    tiles='CartoDB positron',
    max_zoom=14,
    min_zoom=11
)

# Estilo profesional con bordes gruesos
style_function = lambda x: {
    'fillColor': '#87CEEB',
    'fillOpacity': 0.4,
    'color': '#000000',  # Borde negro
    'weight': 3,  # Borde grueso
    'opacity': 1,
    'dashArray': ''
}

# Estilo al hacer hover
highlight_function = lambda x: {
    'fillOpacity': 0.7,
    'weight': 5,
    'color': '#FF0000'
}

# Agregar polígonos (solo geometría, sin columnas extra)
gdf_for_map = dissolved[['Seccional', 'nombre', 'geometry']].copy()

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
            "padding: 8px; "
            "border: 2px solid #000; "
            "border-radius: 4px;"
        )
    )
).add_to(m_folium)

# Agregar etiquetas permanentes en el centro de cada polígono
for idx, row in dissolved.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=DivIcon(html=f"""
            <div style="
                font-family: Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #000000;
                text-align: center;
                text-shadow:
                    -1px -1px 0 #FFF,
                    1px -1px 0 #FFF,
                    -1px 1px 0 #FFF,
                    1px 1px 0 #FFF,
                    0 0 3px #FFF;
                white-space: nowrap;
                pointer-events: none;
            ">
                {row['nombre']}
            </div>
        """)
    ).add_to(m_folium)

m_folium.save('outputs/analysis/map_folium_labels.html')
print("   OK - Guardado: map_folium_labels.html")

# ============================================================================
# OPCIÓN 2: FOLIUM CON NÚMEROS GRANDES (ALTERNATIVA)
# ============================================================================
print("\n3. Creando mapa Folium con números grandes...")

m_folium_nums = folium.Map(
    location=[-31.4201, -64.1888],
    zoom_start=12,
    tiles='CartoDB positron',
    max_zoom=14,
    min_zoom=11
)

# Agregar polígonos
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
            "font-size: 16px; "
            "font-weight: bold; "
            "padding: 10px; "
            "border: 2px solid #000; "
            "border-radius: 4px;"
        )
    )
).add_to(m_folium_nums)

# Etiquetas con solo el número (más limpio)
for idx, row in dissolved.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=DivIcon(html=f"""
            <div style="
                font-family: Arial Black, sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: #000000;
                text-align: center;
                text-shadow:
                    -2px -2px 0 #FFF,
                    2px -2px 0 #FFF,
                    -2px 2px 0 #FFF,
                    2px 2px 0 #FFF,
                    0 0 4px #FFF;
                pointer-events: none;
            ">
                {row['Seccional']}
            </div>
        """)
    ).add_to(m_folium_nums)

m_folium_nums.save('outputs/analysis/map_folium_numbers.html')
print("   OK - Guardado: map_folium_numbers.html")

# ============================================================================
# OPCIÓN 3: PLOTLY CON ETIQUETAS NATIVAS
# ============================================================================
print("\n4. Creando mapa Plotly con etiquetas nativas...")

# Preparar GeoJSON (sin columnas extra)
geojson = json.loads(gdf_for_map.to_json())

# Crear figura
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf_for_map.index,
    z=[1]*len(gdf_for_map),  # Color uniforme
    colorscale=[[0, '#87CEEB'], [1, '#87CEEB']],
    showscale=False,
    marker_opacity=0.5,
    marker_line_width=3,
    marker_line_color='#000000',
    hovertemplate='<b>%{text}</b><extra></extra>',
    text=gdf_for_map['nombre']
))

# Agregar etiquetas de texto como scatter
fig.add_trace(go.Scattermapbox(
    lat=dissolved['lat'],
    lon=dissolved['lon'],
    mode='text',
    text=gdf_for_map['nombre'],
    textfont=dict(
        size=14,
        color='#000000',
        family='Arial Black'
    ),
    textposition='middle center',
    hoverinfo='skip',
    showlegend=False
))

# Layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=11.5,
    mapbox_center={"lat": -31.4201, "lon": -64.1888},
    margin={"r":0, "t":60, "l":0, "b":0},
    title={
        'text': 'Seccionales Electorales - Córdoba Capital<br><sub>Bordes claros + Etiquetas permanentes</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'family': 'Arial'}
    },
    height=700
)

fig.write_html('outputs/analysis/map_plotly_labels.html')
print("   OK - Guardado: map_plotly_labels.html")

# ============================================================================
# OPCIÓN 4: PLOTLY SOLO CON NÚMEROS (MÁS LIMPIO)
# ============================================================================
print("\n5. Creando mapa Plotly solo con números...")

fig_nums = go.Figure(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf_for_map.index,
    z=[1]*len(gdf_for_map),
    colorscale=[[0, '#87CEEB'], [1, '#87CEEB']],
    showscale=False,
    marker_opacity=0.5,
    marker_line_width=3,
    marker_line_color='#000000',
    hovertemplate='<b>Seccional %{text}</b><extra></extra>',
    text=gdf_for_map['Seccional']
))

# Etiquetas solo con números grandes
fig_nums.add_trace(go.Scattermapbox(
    lat=dissolved['lat'],
    lon=dissolved['lon'],
    mode='text',
    text=gdf_for_map['Seccional'],
    textfont=dict(
        size=28,  # Números más grandes
        color='#000000',
        family='Arial Black'
    ),
    textposition='middle center',
    hoverinfo='skip',
    showlegend=False
))

fig_nums.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=11.5,
    mapbox_center={"lat": -31.4201, "lon": -64.1888},
    margin={"r":0, "t":60, "l":0, "b":0},
    title={
        'text': 'Seccionales Electorales - Córdoba Capital<br><sub>Identificación por número</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'family': 'Arial'}
    },
    height=700
)

fig_nums.write_html('outputs/analysis/map_plotly_numbers.html')
print("   OK - Guardado: map_plotly_numbers.html")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*70)
print("MAPAS GENERADOS CON ETIQUETAS VISIBLES - COMPLETO")
print("="*70)
print("\nOpciones creadas:")
print("\n1. map_folium_labels.html")
print("   - Folium con texto 'Seccional X'")
print("   - Bordes negros gruesos (3px)")
print("   - Etiquetas con contorno blanco")
print("\n2. map_folium_numbers.html")
print("   - Folium solo con números grandes")
print("   - Más limpio visualmente")
print("   - Números tamaño 24px")
print("\n3. map_plotly_labels.html")
print("   - Plotly con texto 'Seccional X'")
print("   - Renderizado más rápido")
print("   - Mejor para dashboards")
print("\n4. map_plotly_numbers.html")
print("   - Plotly solo con números")
print("   - Números tamaño 28px")
print("   - MAS LIMPIO Y PROFESIONAL (RECOMENDADO)")
print("\nAbre cada archivo y compara cuál prefieres!")
print()
