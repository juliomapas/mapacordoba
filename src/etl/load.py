"""
Load module - Save processed data to files and database.
"""
import pandas as pd
import geopandas as gpd
import sqlite3
from src.config import settings


def load_to_csv(df: pd.DataFrame) -> None:
    """
    Save electoral data to CSV file.

    Args:
        df: Processed electoral dataframe
    """
    print("[LOAD] Saving to CSV...")

    # Drop original columns if they exist
    cols_to_drop = [col for col in df.columns if col.endswith('_original')]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    df.to_csv(settings.CLEAN_CSV, index=False, encoding='utf-8')

    print(f"[OK] Saved to: {settings.CLEAN_CSV}")


def load_geojson(gdf: gpd.GeoDataFrame) -> None:
    """
    Save geographic data to GeoJSON file.

    Args:
        gdf: Processed geodataframe
    """
    print("[LOAD] Saving GeoJSON...")

    gdf.to_file(settings.SECCIONALES_GEOJSON, driver='GeoJSON', encoding='utf-8')

    print(f"[OK] Saved to: {settings.SECCIONALES_GEOJSON}")


def load_to_database(df: pd.DataFrame, gdf: gpd.GeoDataFrame) -> None:
    """
    Load data to SQLite database with normalized schema.

    Args:
        df: Processed electoral dataframe
        gdf: Processed geodataframe
    """
    print("[LOAD] Loading to database...")

    conn = sqlite3.connect(settings.DATABASE_FILE)

    try:
        # Create tables
        print("  Creating tables...")

        # Seccionales table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seccionales (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE,
                geometry TEXT NOT NULL
            )
        """)

        # Agrupaciones table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agrupaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                color TEXT
            )
        """)

        # Resultados table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anio INTEGER NOT NULL,
                cargo TEXT NOT NULL,
                seccional_id INTEGER NOT NULL,
                agrupacion_id INTEGER NOT NULL,
                votos INTEGER NOT NULL,
                porcentaje REAL,
                total_votos INTEGER,
                FOREIGN KEY (seccional_id) REFERENCES seccionales(id),
                FOREIGN KEY (agrupacion_id) REFERENCES agrupaciones(id)
            )
        """)

        # Create indexes
        conn.execute("CREATE INDEX IF NOT EXISTS idx_resultados_anio ON resultados(anio)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_resultados_seccional ON resultados(seccional_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_resultados_agrupacion ON resultados(agrupacion_id)")

        # Insert seccionales
        print("  Inserting seccionales...")
        for _, row in gdf.iterrows():
            conn.execute(
                "INSERT OR IGNORE INTO seccionales (id, nombre, geometry) VALUES (?, ?, ?)",
                (int(row['seccional']), row['seccional'], row['geometry'].wkt)
            )

        # Insert agrupaciones
        print("  Inserting agrupaciones...")
        from .utils import get_party_colors
        colors = get_party_colors()

        agrupaciones = df['agrupacion'].unique()
        for agrupacion in agrupaciones:
            color = colors.get(agrupacion, '#808080')
            conn.execute(
                "INSERT OR IGNORE INTO agrupaciones (nombre, color) VALUES (?, ?)",
                (agrupacion, color)
            )

        # Get agrupacion IDs
        agrupacion_ids = {}
        cursor = conn.execute("SELECT id, nombre FROM agrupaciones")
        for row in cursor:
            agrupacion_ids[row[1]] = row[0]

        # Insert resultados
        print("  Inserting resultados...")
        for _, row in df.iterrows():
            seccional_id = int(row['seccional'])
            agrupacion_id = agrupacion_ids[row['agrupacion']]

            conn.execute("""
                INSERT INTO resultados
                (anio, cargo, seccional_id, agrupacion_id, votos, porcentaje, total_votos)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row['anio'],
                row['cargo'],
                seccional_id,
                agrupacion_id,
                row['votos'],
                row.get('porcentaje'),
                row.get('total_votos')
            ))

        conn.commit()
        print(f"[OK] Database saved to: {settings.DATABASE_FILE}")

    finally:
        conn.close()


def load_all(df: pd.DataFrame, gdf: gpd.GeoDataFrame) -> None:
    """
    Load data to all destinations (CSV, GeoJSON, Database).

    Args:
        df: Processed electoral dataframe
        gdf: Processed geodataframe
    """
    load_to_csv(df)
    load_geojson(gdf)
    load_to_database(df, gdf)
    print("\n[OK] All data loaded successfully!")


if __name__ == '__main__':
    from .extract import extract_all
    from .transform import transform_electoral_data, transform_geojson, calculate_percentages

    # Test loading
    electoral_dfs, geo_df = extract_all()
    clean_df = transform_electoral_data(electoral_dfs)
    clean_df = calculate_percentages(clean_df)
    geo_seccionales = transform_geojson(geo_df)

    load_all(clean_df, geo_seccionales)
