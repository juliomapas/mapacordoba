"""
Transform module - Clean and normalize electoral data.
"""
import pandas as pd
import geopandas as gpd
from typing import List
from .utils import normalize_seccional, normalize_party_name, normalize_columns


def transform_electoral_data(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Transform and normalize electoral data from multiple years.

    Args:
        dfs: List of dataframes [df_2021, df_2023, df_2025]

    Returns:
        Single normalized dataframe with all years
    """
    print("[TRANSFORM] Transforming electoral data...")

    normalized_dfs = []

    for i, df in enumerate(dfs):
        year = [2021, 2023, 2025][i]
        print(f"  Processing {year}...")

        # Make a copy to avoid modifying original
        df = df.copy()

        # Normalize column names
        df = normalize_columns(df)

        # Ensure required columns exist
        required_cols = ['anio', 'cargo', 'seccional', 'agrupacion', 'votos']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"    Warning: Missing columns {missing} in {year} data")
            continue

        # Select only required columns
        df = df[required_cols].copy()

        # Normalize seccional names
        df['seccional_original'] = df['seccional']
        df['seccional'] = df['seccional'].apply(normalize_seccional)

        # Filter out invalid seccionales (None values)
        invalid_count = df['seccional'].isna().sum()
        if invalid_count > 0:
            print(f"    Filtered {invalid_count} invalid seccional records (likely totals)")
        df = df[df['seccional'].notna()]

        # Normalize party names
        df['agrupacion_original'] = df['agrupacion']
        df['agrupacion'] = df['agrupacion'].apply(normalize_party_name)

        # Ensure votos is integer
        df['votos'] = df['votos'].astype(int)

        # Ensure anio is integer
        df['anio'] = df['anio'].astype(int)

        print(f"    ✓ Processed {len(df)} records for {year}")
        normalized_dfs.append(df)

    # Combine all years
    combined_df = pd.concat(normalized_dfs, ignore_index=True)

    # Sort by year, seccional, votes descending
    combined_df = combined_df.sort_values(['anio', 'seccional', 'votos'], ascending=[True, True, False])

    print(f"[OK] Transformed: {len(combined_df)} total records across {combined_df['anio'].nunique()} years")
    print(f"     Seccionales: {sorted(combined_df['seccional'].unique())}")
    print(f"     Years: {sorted(combined_df['anio'].unique())}")

    return combined_df


def transform_geojson(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Transform GeoJSON by dissolving circuits into seccionales.

    Args:
        gdf: GeoDataFrame with circuit-level data

    Returns:
        GeoDataFrame with seccional-level data (14 polygons)
    """
    print("[TRANSFORM] Transforming geographic data...")

    print(f"  Input: {len(gdf)} circuits")

    # Fix invalid geometries before dissolving
    print("  Fixing invalid geometries...")
    gdf['geometry'] = gdf['geometry'].buffer(0)

    # Dissolve circuits into seccionales
    gdf_seccionales = gdf.dissolve(by='Seccional', as_index=False)

    # Keep only essential columns
    gdf_seccionales = gdf_seccionales[['Seccional', 'geometry']].copy()

    # Rename for consistency
    gdf_seccionales = gdf_seccionales.rename(columns={'Seccional': 'seccional'})

    # Sort by seccional number
    gdf_seccionales['seccional_num'] = gdf_seccionales['seccional'].astype(int)
    gdf_seccionales = gdf_seccionales.sort_values('seccional_num')
    gdf_seccionales = gdf_seccionales.drop('seccional_num', axis=1)

    print(f"[OK] Transformed: {len(gdf_seccionales)} seccionales")

    return gdf_seccionales


def calculate_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate vote percentages for each seccional/year combination.

    Args:
        df: Electoral dataframe

    Returns:
        DataFrame with added percentage columns
    """
    print("[TRANSFORM] Calculating percentages...")

    df = df.copy()

    # Calculate total votes per seccional/year
    totals = df.groupby(['anio', 'seccional'])['votos'].sum().reset_index()
    totals = totals.rename(columns={'votos': 'total_votos'})

    # Merge totals back
    df = df.merge(totals, on=['anio', 'seccional'], how='left')

    # Calculate percentage
    df['porcentaje'] = (df['votos'] / df['total_votos'] * 100).round(2)

    print(f"[OK] Calculated percentages")

    return df


if __name__ == '__main__':
    from .extract import extract_all

    # Test transformation
    electoral_dfs, geo_df = extract_all()

    # Transform electoral data
    clean_df = transform_electoral_data(electoral_dfs)
    clean_df = calculate_percentages(clean_df)

    print("\n📊 Transformed Electoral Data Sample:")
    print(clean_df.head(20))

    print("\n📊 Summary by Year:")
    print(clean_df.groupby('anio').agg({
        'votos': 'sum',
        'seccional': 'nunique',
        'agrupacion': 'nunique'
    }))

    # Transform geographic data
    geo_seccionales = transform_geojson(geo_df)

    print("\n🗺️  Transformed Geographic Data:")
    print(geo_seccionales)
