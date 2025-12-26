"""
Utility functions for ETL process.
"""
import json
from pathlib import Path
from typing import Dict, Optional
from src.config import settings


def load_json_mapping(filepath: Path) -> Dict:
    """Load JSON mapping file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_seccional_mapping() -> Dict[str, Optional[str]]:
    """Get seccional name normalization mapping."""
    return load_json_mapping(settings.SECCIONAL_MAPPING_FILE)


def get_party_normalization() -> Dict[str, str]:
    """Get party name normalization mapping."""
    return load_json_mapping(settings.PARTY_NORMALIZATION_FILE)


def get_party_colors() -> Dict[str, str]:
    """Get party color mapping."""
    return load_json_mapping(settings.PARTY_COLORS_FILE)


def normalize_seccional(seccional: str) -> Optional[str]:
    """
    Normalize seccional name to standard format (numeric string 1-14).

    Args:
        seccional: Original seccional name

    Returns:
        Normalized seccional number as string, or None if invalid
    """
    mapping = get_seccional_mapping()
    return mapping.get(seccional)


def normalize_party_name(party: str) -> str:
    """
    Normalize party name to standard format.

    Args:
        party: Original party name

    Returns:
        Normalized party name
    """
    mapping = get_party_normalization()
    return mapping.get(party, party)


def get_party_color(party: str) -> str:
    """
    Get color for a political party.

    Args:
        party: Party name (preferably normalized)

    Returns:
        Hex color code, or default gray if not found
    """
    colors = get_party_colors()
    return colors.get(party, '#808080')


COLUMN_MAPPING = {
    'a�o': 'anio',
    'año': 'anio',
    'diputados': 'votos',
    'sum_diputados': 'votos',
    'agrupacion': 'agrupacion',
    'seccional': 'seccional',
    'Seccional': 'seccional',
    'cargo': 'cargo'
}


def normalize_columns(df):
    """
    Normalize column names in electoral dataframe.

    Args:
        df: DataFrame with electoral data

    Returns:
        DataFrame with normalized column names
    """
    # First try to decode column names if they have encoding issues
    df.columns = df.columns.str.strip()

    # Rename using mapping
    rename_dict = {}
    for col in df.columns:
        if col in COLUMN_MAPPING:
            rename_dict[col] = COLUMN_MAPPING[col]
        elif 'a' in col and 'o' in col:  # Likely año with encoding issues
            rename_dict[col] = 'anio'

    df = df.rename(columns=rename_dict)

    # Ensure we have 'votos' column (from diputados or sum_diputados)
    if 'diputados' in df.columns and 'votos' not in df.columns:
        df = df.rename(columns={'diputados': 'votos'})
    elif 'sum_diputados' in df.columns and 'votos' not in df.columns:
        df = df.rename(columns={'sum_diputados': 'votos'})

    return df
