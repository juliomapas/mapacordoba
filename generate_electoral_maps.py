"""
Generador de Mapas Electorales Córdoba Capital 2021-2025
Crea mapas con colores por partido ganador usando estilo elegante
"""
import geopandas as gpd
import pandas as pd
import folium
from folium import DivIcon
import json

# ============================================================================
# PALETA DE COLORES ELECTORAL
# ============================================================================
PARTY_COLORS = {
    'LA LIBERTAD AVANZA': '#9370DB',           # Violeta
    'ALIANZA LA LIBERTAD AVANZA': '#9370DB',   # Violeta
    'JUNTOS POR EL CAMBIO': '#FFD700',         # Amarillo
    'HACEMOS POR CÓRDOBA': '#87CEEB',          # Celeste
    'UNIÓN POR LA PATRIA': '#0047AB',          # Azul
    'FRENTE DE IZQUIERDA': '#DC143C',          # Rojo
    'FRENTE DE IZQUIERDA  Y DE TRABAJADORES - UNIDAD': '#DC143C',
    'ENCUENTRO VECINAL CÓRDOBA': '#98D8C8',
    'ALIANZA PROVINCIAS UNIDAS': '#F08080',
    'DEFENDAMOS CÓRDOBA': '#20B2AA',
    'DEFAULT': '#CCCCCC'  # Gris
}

print("="*70)
print("GENERANDO MAPAS ELECTORALES CORDOBA CAPITAL 2021-2025")
print("="*70)

# ============================================================================
# CARGAR DATOS
# ============================================================================
print("\n1. Cargando datos...")

# GeoJSON optimizado
gdf_geo = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf_geo['geometry'] = gdf_geo.geometry.buffer(0)
dissolved = gdf_geo.dissolve(by='Seccional').reset_index()
dissolved['geometry'] = dissolved.geometry.simplify(tolerance=0.001, preserve_topology=True)
dissolved['Seccional'] = dissolved['Seccional'].astype(str)

# Datos electorales
df_electoral = pd.read_csv('data/processed/electoral_data_clean.csv')
df_electoral['seccional'] = df_electoral['seccional'].astype(str)

# Calcular ganadores
ganadores = df_electoral.loc[df_electoral.groupby(['anio', 'seccional'])['votos'].idxmax()]
ganadores = ganadores[['anio', 'seccional', 'agrupacion', 'votos', 'porcentaje', 'total_votos']]

print(f"   - Seccionales: {len(dissolved)}")
print(f"   - Registros electorales: {len(df_electoral)}")
print(f"   - Ganadores calculados: {len(ganadores)}")

# ============================================================================
# FUNCIÓN PARA CREAR MAPA
# ============================================================================
def create_electoral_map(year, ganadores_df, gdf):
    """Crea mapa electoral para un año específico"""

    print(f"\n{year}. Creando mapa para elecciones {year}...")

    # Filtrar ganadores del año
    gan_year = ganadores_df[ganadores_df['anio'] == year].copy()

    if len(gan_year) == 0:
        print(f"   ERROR: No hay datos para {year}")
        return None

    # Merge con geometrías
    gdf_year = gdf.merge(
        gan_year,
        left_on='Seccional',
        right_on='seccional',
        how='left'
    )

    # Calcular centroides
    gdf_year['centroid'] = gdf_year.geometry.centroid
    gdf_year['lat'] = gdf_year['centroid'].y
    gdf_year['lon'] = gdf_year['centroid'].x
    gdf_year['nombre'] = gdf_year['Seccional'].apply(lambda x: f'Seccional {x}')

    # Crear mapa base
    m = folium.Map(
        location=[-31.4201, -64.1888],
        zoom_start=12,
        tiles='CartoDB positron',
        max_zoom=14,
        min_zoom=11
    )

    # Función de estilo por seccional
    def style_function(feature):
        seccional = feature['properties']['Seccional']
        ganador_info = gan_year[gan_year['seccional'] == seccional]

        if len(ganador_info) > 0:
            partido = ganador_info.iloc[0]['agrupacion']
            color = PARTY_COLORS.get(partido, PARTY_COLORS['DEFAULT'])
        else:
            color = PARTY_COLORS['DEFAULT']

        return {
            'fillColor': color,
            'fillOpacity': 0.6,
            'color': '#2E86AB',      # Borde azul elegante
            'weight': 1.5,
            'opacity': 1
        }

    # Función de highlight
    def highlight_function(feature):
        seccional = feature['properties']['Seccional']
        ganador_info = gan_year[gan_year['seccional'] == seccional]

        if len(ganador_info) > 0:
            partido = ganador_info.iloc[0]['agrupacion']
            color = PARTY_COLORS.get(partido, PARTY_COLORS['DEFAULT'])
        else:
            color = PARTY_COLORS['DEFAULT']

        return {
            'fillColor': color,
            'fillOpacity': 0.85,
            'color': '#2E86AB',
            'weight': 2.5,
            'opacity': 1
        }

    # Preparar GeoJSON para Folium
    gdf_for_map = gdf_year[['Seccional', 'nombre', 'agrupacion', 'votos', 'porcentaje', 'total_votos', 'geometry']].copy()

    # Formatear campos para tooltip
    gdf_for_map['votos_formatted'] = gdf_for_map['votos'].apply(lambda x: f'{int(x):,}' if pd.notna(x) else 'N/D')
    gdf_for_map['porcentaje_formatted'] = gdf_for_map['porcentaje'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else 'N/D')
    gdf_for_map['total_votos_formatted'] = gdf_for_map['total_votos'].apply(lambda x: f'{int(x):,}' if pd.notna(x) else 'N/D')

    # Agregar GeoJSON con estilos
    folium.GeoJson(
        gdf_for_map,
        name='Seccionales',
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['nombre', 'agrupacion', 'votos_formatted', 'porcentaje_formatted', 'total_votos_formatted'],
            aliases=['Seccional:', 'Ganador:', 'Votos:', 'Porcentaje:', 'Total votos:'],
            style=(
                "background-color: white; "
                "color: #333333; "
                "font-family: Arial, sans-serif; "
                "font-size: 13px; "
                "padding: 10px; "
                "border: 2px solid #2E86AB; "
                "border-radius: 4px; "
                "box-shadow: 0 2px 4px rgba(0,0,0,0.2);"
            ),
            sticky=False
        )
    ).add_to(m)

    # Agregar etiquetas permanentes
    for idx, row in gdf_year.iterrows():
        if pd.notna(row['lat']) and pd.notna(row['lon']):
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

    # Agregar leyenda
    legend_html = f'''
    <div style="
        position: fixed;
        bottom: 50px;
        right: 50px;
        width: 250px;
        background-color: white;
        border: 2px solid #2E86AB;
        border-radius: 5px;
        padding: 15px;
        font-family: Arial, sans-serif;
        font-size: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        z-index: 9999;
    ">
        <h4 style="margin: 0 0 10px 0; color: #2E86AB; font-size: 14px;">
            ELECCIONES {year}
        </h4>
    '''

    # Agregar partidos presentes en este año
    partidos_year = gan_year['agrupacion'].unique()
    for partido in sorted(partidos_year):
        color = PARTY_COLORS.get(partido, PARTY_COLORS['DEFAULT'])
        count = len(gan_year[gan_year['agrupacion'] == partido])
        legend_html += f'''
        <div style="margin: 5px 0;">
            <span style="
                display: inline-block;
                width: 20px;
                height: 14px;
                background-color: {color};
                border: 1px solid #333;
                margin-right: 8px;
                vertical-align: middle;
            "></span>
            <span style="font-size: 11px;">{partido} ({count})</span>
        </div>
        '''

    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    # Guardar
    filename = f'outputs/analysis/mapa_electoral_{year}.html'
    m.save(filename)

    print(f"   OK - Guardado: {filename}")

    # Resumen de colores
    print(f"   Resumen de ganadores:")
    resumen = gan_year['agrupacion'].value_counts()
    for partido, count in resumen.items():
        print(f"      - {partido}: {count} seccionales")

    return m

# ============================================================================
# GENERAR MAPAS PARA CADA AÑO
# ============================================================================
for year in [2021, 2023, 2025]:
    create_electoral_map(year, ganadores, dissolved)

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*70)
print("MAPAS ELECTORALES GENERADOS EXITOSAMENTE")
print("="*70)
print("\nArchivos creados:")
print("  1. outputs/analysis/mapa_electoral_2021.html")
print("  2. outputs/analysis/mapa_electoral_2023.html")
print("  3. outputs/analysis/mapa_electoral_2025.html")
print("\nCaracteristicas:")
print("  - Colores por partido ganador")
print("  - Bordes azules elegantes (1.5px)")
print("  - Hover effect sutil")
print("  - Etiquetas 'Seccional X' permanentes")
print("  - Tooltip con datos detallados")
print("  - Leyenda con partidos del año")
print("\nAbre cada archivo para ver la evolucion electoral!")
print()
