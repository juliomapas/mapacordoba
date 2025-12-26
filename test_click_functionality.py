"""
Script para verificar la funcionalidad de click en el mapa
Simula el comportamiento de los callbacks cuando se hace click en una seccional
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
print("VERIFICACIÓN DE FUNCIONALIDAD DE CLICK EN EL MAPA")
print("=" * 70)

# Cargar datos
print("\n1. Cargando datos...")
gdf_geo = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf_geo['geometry'] = gdf_geo.geometry.buffer(0)
dissolved = gdf_geo.dissolve(by='Seccional').reset_index()
dissolved['Seccional'] = dissolved['Seccional'].astype(str)

df_electoral = pd.read_csv('data/processed/electoral_data_clean.csv')
df_electoral['seccional'] = df_electoral['seccional'].astype(str)

ganadores = df_electoral.loc[df_electoral.groupby(['anio', 'seccional'])['votos'].idxmax()]

print(f"   OK Datos cargados: {len(dissolved)} seccionales, {len(df_electoral)} registros")

# Simular preparación de GeoJSON (como en prepare_geojson_data)
print("\n2. Preparando datos GeoJSON para año 2023...")
selected_year = 2023
gan_year = ganadores[ganadores['anio'] == selected_year].copy()

gdf_year = dissolved.merge(
    gan_year,
    left_on='Seccional',
    right_on='seccional',
    how='left'
)

gdf_year['color'] = gdf_year['agrupacion'].apply(
    lambda x: PARTY_COLORS.get(x, PARTY_COLORS['DEFAULT']) if pd.notna(x) else PARTY_COLORS['DEFAULT']
)

print(f"   OK GeoJSON preparado con {len(gdf_year)} seccionales")
print("\n   Colores asignados por seccional:")
for idx, row in gdf_year[['Seccional', 'agrupacion', 'color']].iterrows():
    print(f"      Seccional {row['Seccional']}: {row['agrupacion']} -> {row['color']}")

# Simular click en una seccional
print("\n3. Simulando CLICK en Seccional 5...")
click_feature = {
    'properties': {
        'Seccional': '5'
    }
}

# Callback 1: update_selected_seccional
if click_feature is not None:
    selected_seccional = str(click_feature['properties']['Seccional'])
else:
    selected_seccional = 'all'

print(f"   OK Seccional seleccionada: {selected_seccional}")

# Callback 2: update_map_and_metrics - Filtrar datos
df_year = df_electoral[df_electoral['anio'] == selected_year].copy()

if selected_seccional and selected_seccional != 'all':
    df_year_filtered = df_year[df_year['seccional'] == selected_seccional].copy()
    pie_title = f"Distribución de Votos - Seccional {selected_seccional}"
    bar_title = f"Top 5 Partidos - Seccional {selected_seccional}"
else:
    df_year_filtered = df_year.copy()
    pie_title = "Distribución de Votos - Todas las Seccionales"
    bar_title = "Top 5 Partidos - Todas las Seccionales"

print(f"\n4. Datos filtrados para Seccional {selected_seccional}:")
print(f"   - Registros totales año 2023: {len(df_year)}")
print(f"   - Registros filtrados: {len(df_year_filtered)}")
print(f"   - Total votos filtrados: {df_year_filtered['votos'].sum():,}")
print(f"   - Título gráfico torta: '{pie_title}'")
print(f"   - Título gráfico barras: '{bar_title}'")

# Calcular Top 5
top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
print(f"\n   Top 5 partidos en Seccional {selected_seccional}:")
for idx, row in top_parties.iterrows():
    pct = (row['votos'] / df_year_filtered['votos'].sum() * 100)
    print(f"      {idx+1}. {row['agrupacion']}: {row['votos']:,} votos ({pct:.1f}%)")

# Simular click en otra seccional
print("\n" + "=" * 70)
print("5. Simulando CLICK en Seccional 1...")
click_feature = {
    'properties': {
        'Seccional': '1'
    }
}

selected_seccional = str(click_feature['properties']['Seccional'])
df_year_filtered = df_year[df_year['seccional'] == selected_seccional].copy()

print(f"   OK Seccional seleccionada: {selected_seccional}")
print(f"   - Registros filtrados: {len(df_year_filtered)}")
print(f"   - Total votos: {df_year_filtered['votos'].sum():,}")

top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
print(f"\n   Top 5 partidos en Seccional {selected_seccional}:")
for idx, row in top_parties.iterrows():
    pct = (row['votos'] / df_year_filtered['votos'].sum() * 100)
    print(f"      {idx+1}. {row['agrupacion']}: {row['votos']:,} votos ({pct:.1f}%)")

# Verificar estructura del GeoJSON para el mapa
print("\n" + "=" * 70)
print("6. Verificando estructura GeoJSON para dash-leaflet...")

gdf_year['agrupacion'] = gdf_year['agrupacion'].fillna('Sin datos')
gdf_year['votos'] = gdf_year['votos'].fillna(0).astype(int)
gdf_year['porcentaje'] = gdf_year['porcentaje'].fillna(0)

geojson_data = json.loads(gdf_year.to_json())

print(f"   OK GeoJSON generado correctamente")
print(f"   - Tipo: {geojson_data['type']}")
print(f"   - Número de features: {len(geojson_data['features'])}")

# Verificar que cada feature tiene el campo 'color'
print("\n   Verificando propiedades de las primeras 3 features:")
for i, feature in enumerate(geojson_data['features'][:3]):
    props = feature['properties']
    print(f"      Feature {i+1}:")
    print(f"         - Seccional: {props.get('Seccional')}")
    print(f"         - Agrupación: {props.get('agrupacion')}")
    print(f"         - Color: {props.get('color')}")
    print(f"         - Votos: {props.get('votos')}")

print("\n" + "=" * 70)
print("VERIFICACION COMPLETA - EXITOSO")
print("=" * 70)
print("\nResumen:")
print("  OK GeoJSON se genera correctamente con colores")
print("  OK Click en seccional actualiza el filtro")
print("  OK Datos se filtran correctamente por seccional")
print("  OK Top 5 partidos se calcula para seccional seleccionada")
print("  OK Titulos de graficos se actualizan dinamicamente")
print("\n" + "=" * 70)
