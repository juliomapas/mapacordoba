"""
Verificar que los totales del dashboard coincidan con los Excel originales
"""
import pandas as pd
import os

print("=" * 80)
print("VERIFICACION DE TOTALES - EXCEL vs DASHBOARD")
print("=" * 80)

# Leer datos procesados (los que usa el dashboard)
print("\n1. Leyendo datos procesados del dashboard...")
df_dashboard = pd.read_csv('data/processed/electoral_data_clean.csv')
df_dashboard['seccional'] = df_dashboard['seccional'].astype(str)

print(f"   Total registros en CSV procesado: {len(df_dashboard)}")
print(f"   Columnas: {df_dashboard.columns.tolist()}")

# Leer Excel originales
print("\n2. Leyendo archivos Excel originales...")

excel_files = {
    2021: 'data/raw/2021_porseccional_diputados.xls',
    2023: 'data/raw/2023_porseccional_diputados.xlsx',
    2025: 'data/raw/2025_porseccional_diputados.xlsx'
}

excel_data = {}
for year, file_path in excel_files.items():
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        excel_data[year] = df
        print(f"   {year}: {len(df)} registros, columnas: {df.columns.tolist()[:5]}...")
    else:
        print(f"   {year}: ARCHIVO NO ENCONTRADO - {file_path}")

# Verificar año por año
for year in [2021, 2023, 2025]:
    print("\n" + "=" * 80)
    print(f"VERIFICACION AÑO {year}")
    print("=" * 80)

    # Datos del dashboard
    df_year_dashboard = df_dashboard[df_dashboard['anio'] == year].copy()

    print(f"\nDATOS DEL DASHBOARD (CSV procesado):")
    print(f"  Total registros: {len(df_year_dashboard)}")
    print(f"  Total votos: {df_year_dashboard['votos'].sum():,}")

    top5_dashboard = df_year_dashboard.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
    print(f"\n  Top 5 partidos en dashboard:")
    for idx, row in top5_dashboard.iterrows():
        print(f"    {idx+1}. {row['agrupacion']}: {row['votos']:,} votos")

    # Datos del Excel
    if year in excel_data:
        df_excel = excel_data[year]

        # Identificar columnas
        cols = df_excel.columns.tolist()

        # Buscar columna de votos (puede ser 'diputados', 'votos', etc.)
        votos_col = None
        for col in cols:
            if 'diputado' in col.lower() or 'voto' in col.lower():
                votos_col = col
                break

        # Buscar columna de agrupacion
        agrup_col = None
        for col in cols:
            if 'agrupacion' in col.lower() or 'agrupación' in col.lower() or 'partido' in col.lower():
                agrup_col = col
                break

        print(f"\nDATOS DEL EXCEL ORIGINAL:")
        print(f"  Total registros: {len(df_excel)}")

        if votos_col and agrup_col:
            print(f"  Columna votos: '{votos_col}'")
            print(f"  Columna agrupacion: '{agrup_col}'")

            # Filtrar registros válidos (sin totales)
            df_excel_clean = df_excel[df_excel[agrup_col].notna()].copy()

            # Buscar columna de seccional
            secc_col = None
            for col in cols:
                if 'seccional' in col.lower():
                    secc_col = col
                    break

            if secc_col:
                # Filtrar registros que NO son totales
                df_excel_clean = df_excel_clean[df_excel_clean[secc_col].notna()].copy()
                # Convertir a string para comparar
                df_excel_clean[secc_col] = df_excel_clean[secc_col].astype(str)
                # Filtrar solo seccionales 1-14
                df_excel_clean = df_excel_clean[df_excel_clean[secc_col].str.contains('Seccional', na=False)]

            total_votos_excel = df_excel_clean[votos_col].sum()
            print(f"  Total votos (filtrado): {total_votos_excel:,}")

            top5_excel = df_excel_clean.groupby(agrup_col)[votos_col].sum().nlargest(5).reset_index()
            print(f"\n  Top 5 partidos en Excel:")
            for idx, row in top5_excel.iterrows():
                print(f"    {idx+1}. {row[agrup_col]}: {row[votos_col]:,} votos")

            # COMPARACION
            print(f"\n  COMPARACION:")
            diff_votos = df_year_dashboard['votos'].sum() - total_votos_excel
            print(f"    Diferencia total votos: {diff_votos:,}")

            if abs(diff_votos) < 10:
                print(f"    OK Los totales coinciden (diferencia minima)")
            else:
                print(f"    ERROR Hay diferencia significativa!")
                print(f"    Dashboard: {df_year_dashboard['votos'].sum():,}")
                print(f"    Excel:     {total_votos_excel:,}")
        else:
            print(f"  ERROR: No se encontraron columnas de votos o agrupacion")
            print(f"  Columnas disponibles: {cols}")

print("\n" + "=" * 80)
print("VERIFICACION COMPLETA")
print("=" * 80)
