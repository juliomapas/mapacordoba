"""
Mapa electoral definitivo con estilo elegante
- Plotly para performance
- Texto completo "Seccional X"
- Bordes delgados y suaves
"""
import geopandas as gpd
import plotly.graph_objects as go
import json

print("="*70)
print("GENERANDO MAPA ELECTORAL ELEGANTE")
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

# Calcular centroides
dissolved['centroid'] = dissolved.geometry.centroid
dissolved['lat'] = dissolved['centroid'].y
dissolved['lon'] = dissolved['centroid'].x

print(f"   OK - {len(dissolved)} seccionales procesados")

# Preparar GeoJSON limpio
gdf_for_map = dissolved[['Seccional', 'nombre', 'geometry']].copy()
geojson = json.loads(gdf_for_map.to_json())

# ============================================================================
# MAPA ELEGANTE CON BORDES SUAVES
# ============================================================================
print("\n2. Creando mapa con estilo elegante...")

fig = go.Figure()

# Polígonos con bordes delgados
fig.add_trace(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf_for_map.index,
    z=[1]*len(gdf_for_map),
    colorscale=[[0, '#87CEEB'], [1, '#87CEEB']],  # Celeste uniforme
    showscale=False,
    marker_opacity=0.4,  # Transparencia suave
    marker_line_width=1.2,  # Borde delgado y elegante
    marker_line_color='#555555',  # Gris oscuro suave (no negro duro)
    hovertemplate='<b>%{text}</b><extra></extra>',
    text=gdf_for_map['nombre'],
    name='Seccionales'
))

# Etiquetas de texto elegantes
fig.add_trace(go.Scattermapbox(
    lat=dissolved['lat'],
    lon=dissolved['lon'],
    mode='text',
    text=dissolved['nombre'],
    textfont=dict(
        size=13,  # Tamaño moderado, legible pero no invasivo
        color='#1a1a1a',  # Negro suave
        family='Arial, sans-serif'
    ),
    textposition='middle center',
    hoverinfo='skip',
    showlegend=False
))

# Layout profesional
fig.update_layout(
    mapbox_style="carto-positron",  # Base limpia
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
        font_family="Arial"
    )
)

fig.write_html('outputs/analysis/map_final_elegant.html')
print("   OK - Guardado: map_final_elegant.html")

# ============================================================================
# VARIANTE: AÚN MÁS DELICADO
# ============================================================================
print("\n3. Creando variante ultra-delicada...")

fig_delicate = go.Figure()

# Polígonos con bordes muy finos
fig_delicate.add_trace(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf_for_map.index,
    z=[1]*len(gdf_for_map),
    colorscale=[[0, '#87CEEB'], [1, '#87CEEB']],
    showscale=False,
    marker_opacity=0.35,  # Más transparente
    marker_line_width=0.8,  # Bordes muy finos
    marker_line_color='#666666',  # Gris medio
    hovertemplate='<b>%{text}</b><extra></extra>',
    text=gdf_for_map['nombre'],
    name='Seccionales'
))

# Etiquetas con sombra sutil
fig_delicate.add_trace(go.Scattermapbox(
    lat=dissolved['lat'],
    lon=dissolved['lon'],
    mode='text',
    text=dissolved['nombre'],
    textfont=dict(
        size=12,
        color='#2a2a2a',
        family='Arial, sans-serif'
    ),
    textposition='middle center',
    hoverinfo='skip',
    showlegend=False
))

fig_delicate.update_layout(
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
        font_family="Arial"
    )
)

fig_delicate.write_html('outputs/analysis/map_ultra_delicate.html')
print("   OK - Guardado: map_ultra_delicate.html")

# ============================================================================
# VARIANTE: BORDES MEDIOS (BALANCE)
# ============================================================================
print("\n4. Creando variante balanceada...")

fig_balanced = go.Figure()

fig_balanced.add_trace(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf_for_map.index,
    z=[1]*len(gdf_for_map),
    colorscale=[[0, '#87CEEB'], [1, '#87CEEB']],
    showscale=False,
    marker_opacity=0.45,
    marker_line_width=1.5,  # Balance entre delgado y visible
    marker_line_color='#4a4a4a',  # Gris oscuro elegante
    hovertemplate='<b>%{text}</b><extra></extra>',
    text=gdf_for_map['nombre'],
    name='Seccionales'
))

fig_balanced.add_trace(go.Scattermapbox(
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

fig_balanced.update_layout(
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
        font_family="Arial"
    )
)

fig_balanced.write_html('outputs/analysis/map_balanced.html')
print("   OK - Guardado: map_balanced.html")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*70)
print("MAPAS ELEGANTES GENERADOS")
print("="*70)
print("\nSe crearon 3 variantes con diferentes grosores de borde:")
print("\n1. map_final_elegant.html")
print("   - Borde: 1.2px (delgado y elegante)")
print("   - Color borde: Gris oscuro suave (#555)")
print("   - Opacidad: 40%")
print("   - Texto: 'Seccional X' (13px)")
print("\n2. map_ultra_delicate.html")
print("   - Borde: 0.8px (ultra-fino)")
print("   - Color borde: Gris medio (#666)")
print("   - Opacidad: 35% (mas transparente)")
print("   - Texto: 'Seccional X' (12px)")
print("\n3. map_balanced.html")
print("   - Borde: 1.5px (balance)")
print("   - Color borde: Gris oscuro elegante (#4a4a4a)")
print("   - Opacidad: 45%")
print("   - Texto: 'Seccional X' (13px)")
print("\nAbre cada archivo y elige el que mas te guste!")
print("Recomiendo empezar por: map_final_elegant.html")
print()
