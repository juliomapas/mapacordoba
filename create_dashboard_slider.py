"""
Dashboard Electoral con Slider Temporal
Navega entre 2021, 2023 y 2025 con un slider interactivo
"""
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import json

# Paleta de colores
PARTY_COLORS = {
    'LA LIBERTAD AVANZA': '#9370DB',
    'ALIANZA LA LIBERTAD AVANZA': '#9370DB',
    'JUNTOS POR EL CAMBIO': '#FFD700',
    'HACEMOS POR CÓRDOBA': '#87CEEB',
    'UNIÓN POR LA PATRIA': '#0047AB',
    'FRENTE DE IZQUIERDA': '#DC143C',
    'FRENTE DE IZQUIERDA  Y DE TRABAJADORES - UNIDAD': '#DC143C',
    'DEFAULT': '#CCCCCC'
}

print("="*70)
print("CREANDO DASHBOARD CON SLIDER TEMPORAL")
print("="*70)

# Cargar datos
print("\n1. Cargando datos...")
gdf_geo = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf_geo['geometry'] = gdf_geo.geometry.buffer(0)
dissolved = gdf_geo.dissolve(by='Seccional').reset_index()
dissolved['geometry'] = dissolved.geometry.simplify(tolerance=0.001, preserve_topology=True)
dissolved['Seccional'] = dissolved['Seccional'].astype(str)

df_electoral = pd.read_csv('data/processed/electoral_data_clean.csv')
df_electoral['seccional'] = df_electoral['seccional'].astype(str)

# Calcular ganadores
ganadores = df_electoral.loc[df_electoral.groupby(['anio', 'seccional'])['votos'].idxmax()]

# Calcular centroides
dissolved['centroid'] = dissolved.geometry.centroid
dissolved['lat'] = dissolved['centroid'].y
dissolved['lon'] = dissolved['centroid'].x

print(f"   OK - {len(dissolved)} seccionales, {len(ganadores)} ganadores")

# ============================================================================
# CREAR FRAMES POR AÑO
# ============================================================================
print("\n2. Creando frames para cada año...")

frames = []
years = [2021, 2023, 2025]

for year in years:
    print(f"   Procesando año {year}...")

    # Ganadores del año
    gan_year = ganadores[ganadores['anio'] == year].copy()

    # Merge con geometrías
    gdf_year = dissolved.merge(
        gan_year,
        left_on='Seccional',
        right_on='seccional',
        how='left'
    )

    # Asignar colores
    gdf_year['color'] = gdf_year['agrupacion'].apply(
        lambda x: PARTY_COLORS.get(x, PARTY_COLORS['DEFAULT']) if pd.notna(x) else PARTY_COLORS['DEFAULT']
    )

    # Preparar GeoJSON
    gdf_map = gdf_year[['Seccional', 'agrupacion', 'votos', 'porcentaje', 'color', 'geometry']].copy()
    geojson = json.loads(gdf_map.to_json())

    # Crear choropleth para este año
    choropleth = go.Choroplethmapbox(
        geojson=geojson,
        locations=gdf_map.index,
        z=list(range(len(gdf_map))),  # Dummy values
        colorscale=[[i/(len(gdf_map)-1), color] for i, color in enumerate(gdf_map['color'])],
        showscale=False,
        marker_opacity=0.6,
        marker_line_width=1.5,
        marker_line_color='#2E86AB',
        hovertemplate='<b>Seccional %{customdata[0]}</b><br>' +
                      'Ganador: %{customdata[1]}<br>' +
                      'Votos: %{customdata[2]:,}<br>' +
                      'Porcentaje: %{customdata[3]:.1f}%<extra></extra>',
        customdata=gdf_map[['Seccional', 'agrupacion', 'votos', 'porcentaje']].fillna('N/D').values,
        name=str(year)
    )

    # Etiquetas de texto
    text_scatter = go.Scattermapbox(
        lat=gdf_year['lat'],
        lon=gdf_year['lon'],
        mode='text',
        text=gdf_year['Seccional'].apply(lambda x: f'Seccional {x}'),
        textfont=dict(size=13, color='#1a1a1a', family='Arial'),
        hoverinfo='skip',
        showlegend=False,
        name=f'labels_{year}'
    )

    # Frame con ambas trazas
    frames.append(go.Frame(
        data=[choropleth, text_scatter],
        name=str(year),
        layout=go.Layout(
            title_text=f'Elecciones {year} - Córdoba Capital'
        )
    ))

# ============================================================================
# CREAR FIGURA CON SLIDER
# ============================================================================
print("\n3. Configurando dashboard interactivo...")

# Figura inicial (2021)
fig = go.Figure(data=frames[0].data, frames=frames)

# Layout del mapa
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=11.8,
    mapbox_center={"lat": -31.4201, "lon": -64.1888},
    margin={"r":0, "t":80, "l":0, "b":100},
    title={
        'text': 'Evolución Electoral Córdoba Capital 2021-2025',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'family': 'Arial', 'color': '#333'}
    },
    height=750,
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial"
    ),
    # Configuración del slider
    sliders=[{
        'active': 0,
        'yanchor': 'top',
        'y': 0,
        'xanchor': 'left',
        'x': 0.1,
        'currentvalue': {
            'prefix': 'Año: ',
            'visible': True,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#333'}
        },
        'pad': {'b': 10, 't': 50},
        'len': 0.8,
        'steps': [
            {
                'args': [
                    [str(year)],
                    {
                        'frame': {'duration': 500, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    }
                ],
                'label': str(year),
                'method': 'animate'
            }
            for year in years
        ]
    }],
    # Botón de play
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'y': 0.02,
        'x': 0.95,
        'xanchor': 'right',
        'yanchor': 'bottom',
        'buttons': [
            {
                'label': '▶ Play',
                'method': 'animate',
                'args': [
                    None,
                    {
                        'frame': {'duration': 1500, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 500}
                    }
                ]
            },
            {
                'label': '⏸ Pause',
                'method': 'animate',
                'args': [
                    [None],
                    {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }
                ]
            }
        ]
    }]
)

# Guardar
output_file = 'outputs/analysis/dashboard_electoral_slider.html'
fig.write_html(output_file)

print(f"\n   OK - Guardado: {output_file}")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*70)
print("DASHBOARD CON SLIDER CREADO EXITOSAMENTE")
print("="*70)
print(f"\nArchivo: {output_file}")
print("\nCaracteristicas:")
print("  - Slider para navegar entre 2021, 2023, 2025")
print("  - Boton Play para animacion automatica")
print("  - Colores por partido ganador")
print("  - Hover con datos detallados")
print("  - Etiquetas permanentes")
print("\nInstrucciones:")
print("  1. Abre el archivo HTML en tu navegador")
print("  2. Usa el slider para cambiar de año")
print("  3. Click 'Play' para ver la evolucion animada")
print("  4. Pasa el mouse sobre las seccionales para ver datos")
print()
