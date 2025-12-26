"""
Electoral trends analysis module.
"""
import pandas as pd
import sqlite3
from pathlib import Path
from src.config import settings


def load_electoral_data() -> pd.DataFrame:
    """Load processed electoral data from CSV."""
    return pd.read_csv(settings.CLEAN_CSV)


def get_votes_by_year(df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Get total votes by year and party.

    Args:
        df: Electoral dataframe (optional, will load if not provided)

    Returns:
        DataFrame with votes by year and agrupacion
    """
    if df is None:
        df = load_electoral_data()

    return df.groupby(['anio', 'agrupacion'])['votos'].sum().reset_index()


def get_votes_by_seccional(df: pd.DataFrame = None, year: int = None) -> pd.DataFrame:
    """
    Get votes by seccional for a specific year.

    Args:
        df: Electoral dataframe (optional)
        year: Year to filter (optional)

    Returns:
        DataFrame with votes by seccional
    """
    if df is None:
        df = load_electoral_data()

    if year:
        df = df[df['anio'] == year]

    return df.groupby(['seccional', 'agrupacion'])['votos'].sum().reset_index()


def calculate_growth_rate(df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Calculate growth rate of votes for each party between elections.

    Args:
        df: Electoral dataframe (optional)

    Returns:
        DataFrame with growth rates
    """
    if df is None:
        df = load_electoral_data()

    # Get votes by year and party
    yearly = df.groupby(['anio', 'agrupacion'])['votos'].sum().reset_index()

    # Pivot to get years as columns
    pivot = yearly.pivot(index='agrupacion', columns='anio', values='votos').fillna(0)

    # Calculate growth rates
    growth = pd.DataFrame(index=pivot.index)

    if 2023 in pivot.columns and 2021 in pivot.columns:
        growth['growth_2021_2023'] = ((pivot[2023] - pivot[2021]) / pivot[2021] * 100).replace([float('inf'), float('-inf')], 0)

    if 2025 in pivot.columns and 2023 in pivot.columns:
        growth['growth_2023_2025'] = ((pivot[2025] - pivot[2023]) / pivot[2023] * 100).replace([float('inf'), float('-inf')], 0)

    return growth.reset_index()


def get_winner_by_seccional(df: pd.DataFrame = None, year: int = 2023) -> pd.DataFrame:
    """
    Get winning party for each seccional in a given year.

    Args:
        df: Electoral dataframe (optional)
        year: Year to analyze

    Returns:
        DataFrame with winner per seccional
    """
    if df is None:
        df = load_electoral_data()

    # Filter by year
    df_year = df[df['anio'] == year].copy()

    # Get max votes per seccional
    idx = df_year.groupby('seccional')['votos'].idxmax()
    winners = df_year.loc[idx, ['seccional', 'agrupacion', 'votos', 'porcentaje']]

    return winners.sort_values('seccional')


def get_top_parties(df: pd.DataFrame = None, n: int = 5) -> pd.DataFrame:
    """
    Get top N parties by total votes across all years.

    Args:
        df: Electoral dataframe (optional)
        n: Number of top parties to return

    Returns:
        DataFrame with top parties
    """
    if df is None:
        df = load_electoral_data()

    top = df.groupby('agrupacion')['votos'].sum().sort_values(ascending=False).head(n)
    return top.reset_index()


if __name__ == '__main__':
    df = load_electoral_data()

    print("=== Electoral Trends Analysis ===\n")

    print("1. Top 5 parties (all years combined):")
    print(get_top_parties(df))

    print("\n2. Growth rates:")
    print(calculate_growth_rate(df))

    print("\n3. Winners by seccional (2023):")
    print(get_winner_by_seccional(df, 2023))
