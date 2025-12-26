"""
Political analysis module - Volatility, competitiveness, clustering.
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from src.config import settings


def load_electoral_data() -> pd.DataFrame:
    """Load processed electoral data from CSV."""
    return pd.read_csv(settings.CLEAN_CSV)


def calculate_pedersen_index(df: pd.DataFrame = None, year_from: int = 2021, year_to: int = 2023) -> float:
    """
    Calculate Pedersen Volatility Index between two elections.

    The index measures the net change in vote shares between elections.
    Formula: V = 0.5 * Σ|Pi(t) - Pi(t-1)|

    Args:
        df: Electoral dataframe (optional)
        year_from: Starting year
        year_to: Ending year

    Returns:
        Volatility index (percentage)
    """
    if df is None:
        df = load_electoral_data()

    # Get total votes per year per party
    votes_from = df[df['anio'] == year_from].groupby('agrupacion')['votos'].sum()
    votes_to = df[df['anio'] == year_to].groupby('agrupacion')['votos'].sum()

    # Calculate total votes
    total_from = votes_from.sum()
    total_to = votes_to.sum()

    # Calculate percentages
    pct_from = (votes_from / total_from * 100).fillna(0)
    pct_to = (votes_to / total_to * 100).fillna(0)

    # Align indices (parties might not exist in both elections)
    all_parties = set(pct_from.index) | set(pct_to.index)
    pct_from = pct_from.reindex(all_parties, fill_value=0)
    pct_to = pct_to.reindex(all_parties, fill_value=0)

    # Calculate Pedersen index
    volatility = 0.5 * np.abs(pct_to - pct_from).sum()

    return round(volatility, 2)


def identify_competitive_seccionales(df: pd.DataFrame = None, year: int = 2023, threshold: float = 5.0) -> pd.DataFrame:
    """
    Identify competitive seccionales (small margin between 1st and 2nd place).

    Args:
        df: Electoral dataframe (optional)
        year: Year to analyze
        threshold: Maximum percentage difference to consider competitive

    Returns:
        DataFrame with competitive seccionales
    """
    if df is None:
        df = load_electoral_data()

    # Filter by year
    df_year = df[df['anio'] == year].copy()

    competitive = []

    for seccional in df_year['seccional'].unique():
        df_sec = df_year[df_year['seccional'] == seccional].sort_values('votos', ascending=False)

        if len(df_sec) >= 2:
            first = df_sec.iloc[0]
            second = df_sec.iloc[1]

            margin = first['porcentaje'] - second['porcentaje']

            if margin <= threshold:
                competitive.append({
                    'seccional': seccional,
                    'winner': first['agrupacion'],
                    'winner_pct': first['porcentaje'],
                    'runner_up': second['agrupacion'],
                    'runner_up_pct': second['porcentaje'],
                    'margin': round(margin, 2)
                })

    return pd.DataFrame(competitive)


def calculate_concentration_index(df: pd.DataFrame = None, year: int = 2023) -> Dict[str, float]:
    """
    Calculate Herfindahl-Hirschman Index (HHI) for electoral concentration.

    Higher values indicate more concentrated vote (less competitive).

    Args:
        df: Electoral dataframe (optional)
        year: Year to analyze

    Returns:
        Dictionary with HHI per seccional
    """
    if df is None:
        df = load_electoral_data()

    # Filter by year
    df_year = df[df['anio'] == year].copy()

    hhi_dict = {}

    for seccional in df_year['seccional'].unique():
        df_sec = df_year[df_year['seccional'] == seccional]

        # Calculate HHI: sum of squared market shares
        hhi = (df_sec['porcentaje'] ** 2).sum()
        hhi_dict[seccional] = round(hhi, 2)

    return hhi_dict


def analyze_vote_swing(df: pd.DataFrame = None, year_from: int = 2021, year_to: int = 2023) -> pd.DataFrame:
    """
    Analyze vote swing by seccional between two elections.

    Args:
        df: Electoral dataframe (optional)
        year_from: Starting year
        year_to: Ending year

    Returns:
        DataFrame with swing analysis
    """
    if df is None:
        df = load_electoral_data()

    # Get data for both years
    df_from = df[df['anio'] == year_from].copy()
    df_to = df[df['anio'] == year_to].copy()

    swing_results = []

    for seccional in sorted(df['seccional'].unique()):
        # Get winner in each year
        winner_from = df_from[df_from['seccional'] == seccional].sort_values('votos', ascending=False).iloc[0] if len(df_from[df_from['seccional'] == seccional]) > 0 else None
        winner_to = df_to[df_to['seccional'] == seccional].sort_values('votos', ascending=False).iloc[0] if len(df_to[df_to['seccional'] == seccional]) > 0 else None

        if winner_from is not None and winner_to is not None:
            swing_results.append({
                'seccional': seccional,
                f'winner_{year_from}': winner_from['agrupacion'],
                f'winner_{year_to}': winner_to['agrupacion'],
                'flipped': winner_from['agrupacion'] != winner_to['agrupacion']
            })

    return pd.DataFrame(swing_results)


if __name__ == '__main__':
    df = load_electoral_data()

    print("=== Political Analysis ===\n")

    print("1. Pedersen Volatility Index (2021-2023):")
    volatility_2021_2023 = calculate_pedersen_index(df, 2021, 2023)
    print(f"   {volatility_2021_2023}%")

    print("\n2. Pedersen Volatility Index (2023-2025):")
    volatility_2023_2025 = calculate_pedersen_index(df, 2023, 2025)
    print(f"   {volatility_2023_2025}%")

    print("\n3. Competitive Seccionales (2023, margin < 5%):")
    competitive = identify_competitive_seccionales(df, 2023, 5.0)
    print(competitive)

    print("\n4. Vote Swing Analysis (2021-2023):")
    swing = analyze_vote_swing(df, 2021, 2023)
    print(swing)
    print(f"\n   Seccionales that flipped: {swing['flipped'].sum()}")
