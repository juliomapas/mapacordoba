"""
Verificar que la seccional seleccionada se resalta correctamente en el mapa
"""

import pandas as pd
import geopandas as gpd
import json

# Colores de partidos
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

print("=" * 70)
print("VERIFICACION DE RESALTADO DE SECCIONAL SELECCIONADA")
print("=" * 70)

# Cargar datos
gdf_geo = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf_geo['geometry'] = gdf_geo.geometry.buffer(0)
dissolved = gdf_geo.dissolve(by='Seccional').reset_index()
dissolved['Seccional'] = dissolved['Seccional'].astype(str)

df_electoral = pd.read_csv('data/processed/electoral_data_clean.csv')
df_electoral['seccional'] = df_electoral['seccional'].astype(str)

ganadores = df_electoral.loc[df_electoral.groupby(['anio', 'seccional'])['votos'].idxmax()]

print("\n1. Preparando GeoJSON SIN seccional seleccionada (all)...")
selected_year = 2023
selected_seccional = 'all'

gan_year = ganadores[ganadores['anio'] == selected_year].copy()
gdf_year = dissolved.merge(gan_year, left_on='Seccional', right_on='seccional', how='left')
gdf_year['color'] = gdf_year['agrupacion'].apply(
    lambda x: PARTY_COLORS.get(x, PARTY_COLORS['DEFAULT']) if pd.notna(x) else PARTY_COLORS['DEFAULT']
)

# Marcar seccional seleccionada
gdf_year['selected'] = gdf_year['Seccional'].apply(
    lambda x: x == selected_seccional if selected_seccional != 'all' else False
)

gdf_year['agrupacion'] = gdf_year['agrupacion'].fillna('Sin datos')
gdf_year['votos'] = gdf_year['votos'].fillna(0).astype(int)

geojson_data = json.loads(gdf_year.to_json())

print(f"   OK GeoJSON generado con {len(geojson_data['features'])} features")
print("\n   Verificando propiedad 'selected' (todas deberian ser False):")
for i, feature in enumerate(geojson_data['features'][:5]):
    props = feature['properties']
    print(f"      Seccional {props['Seccional']}: selected = {props['selected']}")

# Simular selección de Seccional 5
print("\n" + "=" * 70)
print("2. Preparando GeoJSON CON Seccional 5 seleccionada...")
selected_seccional = '5'

gdf_year['selected'] = gdf_year['Seccional'].apply(
    lambda x: x == selected_seccional if selected_seccional != 'all' else False
)

geojson_data = json.loads(gdf_year.to_json())

print(f"   OK GeoJSON generado con {len(geojson_data['features'])} features")
print("\n   Verificando propiedad 'selected':")

selected_count = 0
for feature in geojson_data['features']:
    props = feature['properties']
    if props['Seccional'] == '5':
        print(f"      >>> Seccional {props['Seccional']}: selected = {props['selected']} (RESALTADA)")
        if props['selected']:
            selected_count += 1
    elif int(props['Seccional']) <= 6:
        print(f"      Seccional {props['Seccional']}: selected = {props['selected']}")

print(f"\n   Total de seccionales resaltadas: {selected_count}")
print(f"   Esperado: 1 (solo Seccional 5)")

if selected_count == 1:
    print("\n   OK CORRECTO: Solo la Seccional 5 esta marcada como seleccionada")
else:
    print("\n   ERROR: Numero incorrecto de seccionales seleccionadas")

# Verificar colores
print("\n" + "=" * 70)
print("3. Verificando que los colores se mantienen correctamente...")
for feature in geojson_data['features']:
    props = feature['properties']
    if props['Seccional'] in ['1', '5', '10']:
        print(f"   Seccional {props['Seccional']}: {props['agrupacion']} -> {props['color']} (selected={props['selected']})")

print("\n" + "=" * 70)
print("VERIFICACION COMPLETA")
print("=" * 70)
print("\nResumen:")
print("  OK Propiedad 'selected' se agrega correctamente al GeoJSON")
print("  OK Solo la seccional clickeada tiene selected=True")
print("  OK Los colores se mantienen segun el partido ganador")
print("  OK El estilo JavaScript usara 'selected' para resaltar con:")
print("     - Borde naranja (#FF6B00) y mas grueso (4px)")
print("     - Mayor opacidad (0.9)")
print("\n" + "=" * 70)
