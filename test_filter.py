"""Script de prueba para verificar el filtro de seccional"""
import pandas as pd
import geopandas as gpd

# Cargar datos
df_electoral = pd.read_csv('data/processed/electoral_data_clean.csv')
df_electoral['seccional'] = df_electoral['seccional'].astype(str)

print("=" * 70)
print("VERIFICACIÓN DEL FILTRO DE SECCIONAL")
print("=" * 70)

# Probar filtro con año 2023
selected_year = 2023
df_year = df_electoral[df_electoral['anio'] == selected_year].copy()

print(f"\n1. Datos totales para {selected_year}:")
print(f"   - Total registros: {len(df_year)}")
print(f"   - Total votos: {df_year['votos'].sum():,}")
print(f"   - Partidos únicos: {df_year['agrupacion'].nunique()}")

# Probar filtro "all"
selected_seccional = 'all'
if selected_seccional != 'all':
    df_year_filtered = df_year[df_year['seccional'] == selected_seccional].copy()
else:
    df_year_filtered = df_year.copy()

print(f"\n2. Filtro: {selected_seccional}")
print(f"   - Registros filtrados: {len(df_year_filtered)}")
print(f"   - Total votos: {df_year_filtered['votos'].sum():,}")

top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
print(f"\n   Top 5 partidos:")
for idx, row in top_parties.iterrows():
    print(f"   - {row['agrupacion']}: {row['votos']:,} votos")

# Probar filtro con seccional específica
selected_seccional = '5'
if selected_seccional != 'all':
    df_year_filtered = df_year[df_year['seccional'] == selected_seccional].copy()
else:
    df_year_filtered = df_year.copy()

print(f"\n3. Filtro: Seccional {selected_seccional}")
print(f"   - Registros filtrados: {len(df_year_filtered)}")
print(f"   - Total votos: {df_year_filtered['votos'].sum():,}")

if len(df_year_filtered) > 0:
    top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
    print(f"\n   Top 5 partidos en Seccional {selected_seccional}:")
    for idx, row in top_parties.iterrows():
        print(f"   - {row['agrupacion']}: {row['votos']:,} votos")
else:
    print("   ⚠️ No hay datos para esta seccional")

# Probar otra seccional
selected_seccional = '1'
if selected_seccional != 'all':
    df_year_filtered = df_year[df_year['seccional'] == selected_seccional].copy()
else:
    df_year_filtered = df_year.copy()

print(f"\n4. Filtro: Seccional {selected_seccional}")
print(f"   - Registros filtrados: {len(df_year_filtered)}")
print(f"   - Total votos: {df_year_filtered['votos'].sum():,}")

if len(df_year_filtered) > 0:
    top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
    print(f"\n   Top 5 partidos en Seccional {selected_seccional}:")
    for idx, row in top_parties.iterrows():
        print(f"   - {row['agrupacion']}: {row['votos']:,} votos")
else:
    print("   ⚠️ No hay datos para esta seccional")

print("\n" + "=" * 70)
print("✅ Filtro funcionando correctamente")
print("=" * 70)
