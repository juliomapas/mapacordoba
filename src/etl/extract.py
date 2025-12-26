"""
Extract module - Read raw electoral data files.
"""
import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Tuple, List
from src.config import settings


def extract_electoral_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Extract electoral data from Excel files for 2021, 2023, and 2025.

    Returns:
        Tuple of (df_2021, df_2023, df_2025)
    """
    print("[EXTRACT] Extracting electoral data...")

    # Read 2021 data (XLS format with encoding issues)
    print("  Reading 2021 data...")
    df_2021 = pd.read_excel(
        settings.ELECTORAL_2021,
        engine='xlrd'
    )

    # Read 2023 data (XLSX format)
    print("  Reading 2023 data...")
    df_2023 = pd.read_excel(
        settings.ELECTORAL_2023,
        engine='openpyxl'
    )

    # Read 2025 data (XLSX format)
    print("  Reading 2025 data...")
    df_2025 = pd.read_excel(
        settings.ELECTORAL_2025,
        engine='openpyxl'
    )

    print(f"[OK] Extracted: 2021={len(df_2021)} rows, 2023={len(df_2023)} rows, 2025={len(df_2025)} rows")

    return df_2021, df_2023, df_2025


def extract_geojson() -> gpd.GeoDataFrame:
    """
    Extract geographic data from GeoJSON file.

    Returns:
        GeoDataFrame with electoral circuits
    """
    print("[EXTRACT] Extracting geographic data...")

    gdf = gpd.read_file(settings.GEOJSON_FILE, encoding='utf-8')

    print(f"[OK] Extracted: {len(gdf)} circuit features")

    return gdf


def extract_all() -> Tuple[List[pd.DataFrame], gpd.GeoDataFrame]:
    """
    Extract all data sources.

    Returns:
        Tuple of (list of electoral dataframes, geodataframe)
    """
    electoral_dfs = list(extract_electoral_data())
    geo_df = extract_geojson()

    return electoral_dfs, geo_df


if __name__ == '__main__':
    # Test extraction
    df_2021, df_2023, df_2025 = extract_electoral_data()
    gdf = extract_geojson()

    print("\n📊 2021 Sample:")
    print(df_2021.head())
    print(f"\nColumns: {df_2021.columns.tolist()}")

    print("\n📊 2023 Sample:")
    print(df_2023.head())

    print("\n📊 2025 Sample:")
    print(df_2025.head())

    print("\n🗺️  GeoJSON Sample:")
    print(gdf.head())
    print(f"\nProperties: {gdf.columns.tolist()}")
