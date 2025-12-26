"""
Debug discrepancia en ALIANZA LA LIBERTAD AVANZA 2025
Usuario reporta: Excel suma 272,354 pero dashboard muestra 320,745
"""
import pandas as pd

print("=" * 80)
print("DEBUG: ALIANZA LA LIBERTAD AVANZA - AÑO 2025")
print("=" * 80)

# 1. Leer Excel original
print("\n1. EXCEL ORIGINAL:")
df_excel = pd.read_excel('data/raw/2025_porseccional_diputados.xlsx')
print(f"Total registros: {len(df_excel)}")
print(f"Columnas: {df_excel.columns.tolist()}")

# Filtrar solo ALIANZA LA LIBERTAD AVANZA
df_lla_excel = df_excel[df_excel['agrupacion'].str.contains('LIBERTAD AVANZA', na=False)].copy()
print(f"\nRegistros de LA LIBERTAD AVANZA en Excel: {len(df_lla_excel)}")
print(f"\nDetalle por seccional:")
print(df_lla_excel[['seccional', 'agrupacion', 'diputados']].to_string())

total_excel = df_lla_excel['diputados'].sum()
print(f"\n*** TOTAL EN EXCEL: {total_excel:,} votos ***")

# 2. Leer CSV procesado
print("\n" + "=" * 80)
print("2. CSV PROCESADO (usado por dashboard):")
df_csv = pd.read_csv('data/processed/electoral_data_clean.csv')
df_csv_2025 = df_csv[df_csv['anio'] == 2025].copy()

df_lla_csv = df_csv_2025[df_csv_2025['agrupacion'].str.contains('LIBERTAD AVANZA', na=False)].copy()
print(f"\nRegistros de LA LIBERTAD AVANZA en CSV: {len(df_lla_csv)}")
print(f"\nDetalle por seccional:")
print(df_lla_csv[['seccional', 'agrupacion', 'votos']].to_string())

total_csv = df_lla_csv['votos'].sum()
print(f"\n*** TOTAL EN CSV: {total_csv:,} votos ***")

# 3. Comparación
print("\n" + "=" * 80)
print("3. COMPARACION:")
print(f"Excel:     {total_excel:,} votos")
print(f"CSV:       {total_csv:,} votos")
print(f"Dashboard: 320,745 votos (según usuario)")
diferencia = total_csv - total_excel
print(f"Diferencia: {diferencia:,} votos")

# 4. Buscar duplicados o registros extras
print("\n" + "=" * 80)
print("4. BUSCAR DUPLICADOS:")

# Agrupar por seccional en Excel
print("\nSuma por seccional en EXCEL:")
excel_por_secc = df_lla_excel.groupby('seccional')['diputados'].sum().reset_index()
print(excel_por_secc.to_string())

# Agrupar por seccional en CSV
print("\nSuma por seccional en CSV:")
csv_por_secc = df_lla_csv.groupby('seccional')['votos'].sum().reset_index()
print(csv_por_secc.to_string())

# 5. Verificar si hay múltiples agrupaciones con "LIBERTAD AVANZA"
print("\n" + "=" * 80)
print("5. VERIFICAR VARIANTES DEL NOMBRE:")

print("\nEn Excel:")
print(df_lla_excel['agrupacion'].unique())

print("\nEn CSV:")
print(df_lla_csv['agrupacion'].unique())

# 6. Ver TODOS los registros 2025 con LIBERTAD AVANZA
print("\n" + "=" * 80)
print("6. TODOS LOS REGISTROS 2025 (incluyendo posibles variantes):")
df_all_lla = df_csv_2025[df_csv_2025['agrupacion'].str.contains('LIBERTAD|AVANZA', na=False)].copy()
print(f"\nTotal registros encontrados: {len(df_all_lla)}")
print(f"\nAgrupaciones encontradas:")
for agrup in df_all_lla['agrupacion'].unique():
    votos_agrup = df_all_lla[df_all_lla['agrupacion'] == agrup]['votos'].sum()
    print(f"  - {agrup}: {votos_agrup:,} votos")

total_all = df_all_lla['votos'].sum()
print(f"\n*** TOTAL DE TODOS LOS REGISTROS CON 'LIBERTAD' O 'AVANZA': {total_all:,} votos ***")

print("\n" + "=" * 80)
