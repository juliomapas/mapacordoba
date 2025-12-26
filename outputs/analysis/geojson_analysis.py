"""
Análisis comparativo de calidad geoespacial del GeoJSON
Genera visualizaciones para evaluar diferentes niveles de simplificación
"""
import geopandas as gpd
import folium
from folium import GeoJson
import matplotlib.pyplot as plt
import json

# Cargar y reparar geometrías
print("Cargando GeoJSON original...")
gdf = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
print(f"  Features: {len(gdf)}")
print(f"  Geometrías válidas: {gdf.geometry.is_valid.sum()}/{len(gdf)}")

# Reparar geometrías inválidas
print("\nReparando geometrías...")
gdf['geometry'] = gdf.geometry.buffer(0)
print(f"  Geometrías válidas: {gdf.geometry.is_valid.sum()}/{len(gdf)}")

# Disolver por seccional
print("\nDisolviendo por seccional...")
dissolved = gdf.dissolve(by='Seccional').reset_index()
print(f"  Seccionales: {len(dissolved)}")

# Función auxiliar
def count_vertices(geom):
    if geom.geom_type == 'Polygon':
        return len(geom.exterior.coords)
    elif geom.geom_type == 'MultiPolygon':
        return sum(len(p.exterior.coords) for p in geom.geoms)
    return 0

# Crear mapas comparativos
print("\n" + "="*70)
print("GENERANDO MAPAS COMPARATIVOS")
print("="*70)

configs = [
    ('original', None, 'GeoJSON Original (8,105 vértices)'),
    ('simplified_0001', 0.001, 'Simplificado 0.001 (~1,000 vértices) - RECOMENDADO'),
    ('simplified_0002', 0.002, 'Simplificado 0.002 (~200 vértices)'),
    ('simplified_0005', 0.005, 'Simplificado 0.005 (~130 vértices)')
]

for name, tolerance, title in configs:
    print(f"\nCreando mapa: {title}")

    # Simplificar si aplica
    if tolerance:
        gdf_map = dissolved.copy()
        gdf_map['geometry'] = gdf_map.geometry.simplify(
            tolerance=tolerance,
            preserve_topology=True
        )
    else:
        gdf_map = dissolved.copy()

    # Estadísticas
    vertices = gdf_map.geometry.apply(count_vertices).sum()
    print(f"  Total vértices: {vertices:,}")

    # Crear mapa Folium
    m = folium.Map(
        location=[-31.4201, -64.1888],
        zoom_start=12,
        tiles='CartoDB positron'
    )

    # Estilo base
    style_base = {
        'fillColor': '#3388ff',
        'fillOpacity': 0.5,
        'color': '#666',
        'weight': 2
    }

    # Agregar GeoJSON
    GeoJson(
        gdf_map,
        name='Seccionales',
        style_function=lambda x: style_base,
        tooltip=folium.GeoJsonTooltip(
            fields=['Seccional'],
            aliases=['Seccional:'],
            sticky=True
        )
    ).add_to(m)

    # Guardar
    output_file = f'outputs/analysis/map_{name}.html'
    m.save(output_file)
    print(f"  Guardado: {output_file}")

print("\n" + "="*70)
print("COMPARACIÓN VISUAL GENERADA")
print("="*70)
print("\nRevisa los archivos HTML en outputs/analysis/")
print("Abre cada uno en tu navegador para comparar la calidad visual.")
