"""
Verificación exhaustiva: TODOS los partidos de TODOS los años
Dashboard vs Excel original
"""
import pandas as pd

print("=" * 100)
print("VERIFICACION EXHAUSTIVA: TODOS LOS PARTIDOS - TODOS LOS AÑOS")
print("=" * 100)

# Archivos
files = {
    2021: 'data/raw/2021_porseccional_diputados.xls',
    2023: 'data/raw/2023_porseccional_diputados.xlsx',
    2025: 'data/raw/2025_porseccional_diputados.xlsx'
}

# Leer CSV procesado (dashboard)
df_dashboard = pd.read_csv('data/processed/electoral_data_clean.csv')

# Verificar cada año
for year in [2021, 2023, 2025]:
    print("\n" + "=" * 100)
    print(f"AÑO {year}")
    print("=" * 100)

    # Leer Excel
    df_excel = pd.read_excel(files[year])

    # Datos del dashboard para este año
    df_dash_year = df_dashboard[df_dashboard['anio'] == year].copy()

    # Agrupar por partido - EXCEL
    excel_totals = df_excel.groupby('agrupacion')['diputados'].sum().sort_values(ascending=False)

    # Agrupar por partido - DASHBOARD
    dash_totals = df_dash_year.groupby('agrupacion')['votos'].sum().sort_values(ascending=False)

    print(f"\nTotal de partidos en Excel: {len(excel_totals)}")
    print(f"Total de partidos en Dashboard: {len(dash_totals)}")

    # Crear comparación lado a lado
    print(f"\n{'PARTIDO':<60} {'EXCEL':>15} {'DASHBOARD':>15} {'DIFF':>15}")
    print("-" * 105)

    # Obtener todos los partidos únicos
    all_parties_excel = set(excel_totals.index)
    all_parties_dash = set(dash_totals.index)
    all_parties = all_parties_excel.union(all_parties_dash)

    total_diff = 0
    discrepancies = []

    for party in sorted(all_parties):
        excel_val = excel_totals.get(party, 0)
        dash_val = dash_totals.get(party, 0)
        diff = dash_val - excel_val

        # Nombre del partido (truncado para display)
        party_display = party[:58] if len(party) > 58 else party

        if diff != 0:
            print(f"{party_display:<60} {excel_val:>15,} {dash_val:>15,} {diff:>15,} ** DIFF **")
            discrepancies.append({
                'partido': party,
                'excel': excel_val,
                'dashboard': dash_val,
                'diff': diff
            })
        else:
            print(f"{party_display:<60} {excel_val:>15,} {dash_val:>15,} {diff:>15,}")

        total_diff += abs(diff)

    # Resumen
    print("-" * 105)
    total_excel = excel_totals.sum()
    total_dash = dash_totals.sum()
    print(f"{'TOTAL GENERAL':<60} {total_excel:>15,} {total_dash:>15,} {total_dash - total_excel:>15,}")

    if total_diff == 0:
        print(f"\nOK - TODOS LOS PARTIDOS COINCIDEN PERFECTAMENTE")
    else:
        print(f"\nERROR - HAY DISCREPANCIAS (diferencia total absoluta: {total_diff:,})")
        print(f"\nPartidos con diferencias:")
        for disc in discrepancies:
            print(f"  - {disc['partido']}")
            print(f"    Excel: {disc['excel']:,} | Dashboard: {disc['dashboard']:,} | Diff: {disc['diff']:,}")

    # Verificar si hay partidos solo en uno
    only_excel = all_parties_excel - all_parties_dash
    only_dash = all_parties_dash - all_parties_excel

    if only_excel:
        print(f"\nALERTA - Partidos SOLO en Excel (no en dashboard):")
        for party in only_excel:
            print(f"  - {party}: {excel_totals[party]:,} votos")

    if only_dash:
        print(f"\nALERTA - Partidos SOLO en Dashboard (no en excel):")
        for party in only_dash:
            print(f"  - {party}: {dash_totals[party]:,} votos")

print("\n" + "=" * 100)
print("VERIFICACION COMPLETA")
print("=" * 100)
