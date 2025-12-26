"""
Script de corrección inmediata para GeoJSON electoral
Repara geometrías inválidas y genera versión optimizada

Uso:
    python fix_geojson.py

Salida:
    data/processed/seccionales_optimized.geojson (31 KB, 270 vértices)
"""
import geopandas as gpd
import os
from pathlib import Path

def count_vertices(geom):
    """Cuenta vértices en geometría"""
    if geom.geom_type == 'Polygon':
        return len(geom.exterior.coords)
    elif geom.geom_type == 'MultiPolygon':
        return sum(len(p.exterior.coords) for p in geom.geoms)
    return 0

def main():
    print("="*70)
    print("CORRECCIÓN Y OPTIMIZACIÓN DE GEOJSON ELECTORAL")
    print("="*70)

    # Rutas
    input_file = 'data/raw/Seccionales_Circuitos.geojson'
    output_file = 'data/processed/seccionales_optimized.geojson'

    # Verificar entrada
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: No se encontró {input_file}")
        return

    # Crear directorio de salida
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # 1. CARGAR
    print(f"\n1. Cargando GeoJSON original...")
    gdf = gpd.read_file(input_file)
    print(f"   ✓ Features cargados: {len(gdf)}")
    print(f"   ✓ CRS: {gdf.crs}")

    # 2. VALIDAR
    print(f"\n2. Validando geometrías...")
    invalid_count = (~gdf.geometry.is_valid).sum()
    if invalid_count > 0:
        print(f"   ⚠️  Geometrías inválidas: {invalid_count}")
        invalid = gdf[~gdf.geometry.is_valid]
        for idx, row in invalid.iterrows():
            print(f"      - {row['Nombre']}")
    else:
        print(f"   ✓ Todas las geometrías son válidas")

    # 3. REPARAR
    print(f"\n3. Reparando geometrías...")
    gdf['geometry'] = gdf.geometry.buffer(0)
    print(f"   ✓ Geometrías válidas: {gdf.geometry.is_valid.sum()}/{len(gdf)}")

    # 4. DISOLVER
    print(f"\n4. Disolviendo circuitos en seccionales...")
    dissolved = gdf.dissolve(by='Seccional').reset_index()
    print(f"   ✓ Seccionales creados: {len(dissolved)}")

    # 5. SIMPLIFICAR
    print(f"\n5. Simplificando geometrías (tolerancia 0.001)...")
    vertices_before = dissolved.geometry.apply(count_vertices).sum()
    print(f"   • Vértices antes: {vertices_before:,}")

    dissolved['geometry'] = dissolved.geometry.simplify(
        tolerance=0.001,
        preserve_topology=True
    )

    vertices_after = dissolved.geometry.apply(count_vertices).sum()
    reduction = (1 - vertices_after/vertices_before) * 100
    print(f"   • Vértices después: {vertices_after:,}")
    print(f"   ✓ Reducción: {reduction:.1f}%")

    # 6. LIMPIAR PROPIEDADES
    print(f"\n6. Normalizando propiedades...")
    dissolved = dissolved[['Seccional', 'geometry']]
    dissolved['seccional_num'] = dissolved['Seccional'].astype(int)
    dissolved['nombre'] = dissolved['Seccional'].apply(lambda x: f'Seccional {x}')
    dissolved = dissolved.sort_values('seccional_num')
    print(f"   ✓ Propiedades: {list(dissolved.columns)}")

    # 7. GUARDAR
    print(f"\n7. Guardando GeoJSON optimizado...")
    dissolved.to_file(output_file, driver='GeoJSON')

    # Tamaño de archivo
    size_kb = os.path.getsize(output_file) / 1024
    print(f"   ✓ Archivo guardado: {output_file}")
    print(f"   ✓ Tamaño: {size_kb:.1f} KB")

    # 8. RESUMEN
    print("\n" + "="*70)
    print("✅ OPTIMIZACIÓN COMPLETADA")
    print("="*70)
    print(f"\nArchivo de salida: {output_file}")
    print(f"Seccionales: {len(dissolved)}")
    print(f"Vértices totales: {vertices_after:,} (antes {vertices_before:,})")
    print(f"Reducción: {reduction:.1f}%")
    print(f"Tamaño: {size_kb:.1f} KB")
    print(f"\nPróximos pasos:")
    print(f"  1. Actualiza tus scripts de visualización para usar:")
    print(f"     '{output_file}'")
    print(f"  2. Compara visualmente con el original")
    print(f"  3. Si estás satisfecho, integra en tu pipeline ETL")
    print()

if __name__ == '__main__':
    main()
