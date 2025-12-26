"""
Configuration settings for the electoral visualization project.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
MAPPINGS_DIR = DATA_DIR / 'mappings'

# Output directories
OUTPUT_DIR = BASE_DIR / 'outputs'
MAPS_DIR = OUTPUT_DIR / 'maps'
REPORTS_DIR = OUTPUT_DIR / 'reports'
FIGURES_DIR = OUTPUT_DIR / 'figures'

# Ensure output directories exist
MAPS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Data files
ELECTORAL_2021 = RAW_DATA_DIR / '2021_porseccional_diputados.xls'
ELECTORAL_2023 = RAW_DATA_DIR / '2023_porseccional_diputados.xlsx'
ELECTORAL_2025 = RAW_DATA_DIR / '2025_porseccional_diputados.xlsx'
GEOJSON_FILE = RAW_DATA_DIR / 'Seccionales_Circuitos.geojson'

# Processed files
CLEAN_CSV = PROCESSED_DATA_DIR / 'electoral_data_clean.csv'
SECCIONALES_GEOJSON = PROCESSED_DATA_DIR / 'seccionales_geo.geojson'
DATABASE_FILE = PROCESSED_DATA_DIR / 'electoral_database.db'

# Mapping files
SECCIONAL_MAPPING_FILE = MAPPINGS_DIR / 'seccional_names.json'
PARTY_COLORS_FILE = MAPPINGS_DIR / 'party_colors.json'
PARTY_NORMALIZATION_FILE = MAPPINGS_DIR / 'party_normalization.json'

# Map settings
CORDOBA_CENTER = [-31.4201, -64.1888]
DEFAULT_ZOOM = 12

# Electoral years
YEARS = [2021, 2023, 2025]

# Database settings
DB_ECHO = False  # Set to True for SQL debugging
