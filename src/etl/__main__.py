"""
Main ETL pipeline execution.
Run with: python -m src.etl
"""
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from .extract import extract_all
from .transform import transform_electoral_data, transform_geojson, calculate_percentages
from .load import load_all


def run_etl_pipeline():
    """Execute complete ETL pipeline."""
    print("=" * 60)
    print("Starting ETL Pipeline")
    print("=" * 60)

    # Extract
    print("\n[1/3] EXTRACT")
    electoral_dfs, geo_df = extract_all()

    # Transform
    print("\n[2/3] TRANSFORM")
    clean_df = transform_electoral_data(electoral_dfs)
    clean_df = calculate_percentages(clean_df)
    geo_seccionales = transform_geojson(geo_df)

    # Load
    print("\n[3/3] LOAD")
    load_all(clean_df, geo_seccionales)

    print("\n" + "=" * 60)
    print("ETL Pipeline Completed Successfully!")
    print("=" * 60)

    # Summary statistics
    print("\nSUMMARY STATISTICS:")
    print(f"Total records: {len(clean_df)}")
    print(f"Years: {sorted(clean_df['anio'].unique())}")
    print(f"Seccionales: {len(clean_df['seccional'].unique())}")
    print(f"Political parties: {len(clean_df['agrupacion'].unique())}")
    print(f"\nTop 5 parties by total votes:")
    top_parties = clean_df.groupby('agrupacion')['votos'].sum().sort_values(ascending=False).head()
    for party, votes in top_parties.items():
        print(f"  - {party}: {votes:,} votos")


if __name__ == '__main__':
    run_etl_pipeline()
