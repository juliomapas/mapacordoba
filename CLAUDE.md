# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Electoral visualization and political analysis system for Córdoba Capital's 14 electoral sections (seccionales), tracking voting evolution across 2021, 2023, and 2025 elections.

## Key Commands

### Development Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Data Processing
```bash
# Run complete ETL pipeline
python -m src.etl.extract
python -m src.etl.transform
python -m src.etl.load

# Or run all at once
python -m src.etl
```

### Analysis
```bash
# Generate electoral analysis
python -m src.analysis.electoral_trends

# Run political analysis
python -m src.analysis.political_analysis
```

### Visualization
```bash
# Generate choropleth map
python -m src.visualization.maps --year 2023 --output outputs/maps/

# Create interactive dashboard
python -m src.visualization.dashboard
```

### Jupyter Notebooks
```bash
# Start Jupyter
jupyter notebook

# Navigate to notebooks/ directory
# Start with 01_exploratory_analysis.ipynb
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_etl.py

# Run with coverage
pytest --cov=src tests/
```

## Architecture

### Data Flow
1. **Raw Data** (`data/raw/`): Original Excel files (2021, 2023, 2025) + GeoJSON
2. **ETL Pipeline** (`src/etl/`): Extract → Transform → Load
3. **Processed Data** (`data/processed/`): Cleaned CSV + normalized GeoJSON + SQLite DB
4. **Analysis** (`src/analysis/`): Electoral trends, political insights, statistics
5. **Visualization** (`src/visualization/`): Maps, charts, dashboards
6. **Outputs** (`outputs/`): Generated maps, reports, figures

### Critical Data Issues (UPDATED - Normalized Data)

#### 1. Seccional Name Normalization
Electoral data now uses **consistent naming across all years**:
- **All years (2021, 2023, 2025)**: "Seccional 1" through "Seccional 14"
- **GeoJSON**: Numeric strings "1" through "14"

**ETL Process**: The mapping in `data/mappings/seccional_names.json` converts "Seccional X" → "X" (numeric string).

**Note**: The 2025 file uses "Seccional" (capital S) as column name, but the values are the same format.

#### 2. Vote Column Names (UPDATED)
- **All years (2021, 2023, 2025)**: Uses `diputados` (deputies/votes)

**Transform step renames** `diputados` → `votos` for consistency in the processed data.

#### 3. Special Records
**Updated data no longer contains special total records** - all records now have valid seccional values.

#### 4. Geographic Data
- GeoJSON contains **120 features** (electoral circuits)
- Must be dissolved/aggregated by `Seccional` property to get **14 seccional polygons**
- Use GeoPandas `.dissolve(by='Seccional')` method

### Database Schema

```sql
-- Core tables in data/processed/electoral_database.db

seccionales (
  id INTEGER PRIMARY KEY,
  nombre TEXT,  -- "1" through "14"
  geometry TEXT -- GeoJSON
)

agrupaciones (
  id INTEGER PRIMARY KEY,
  nombre TEXT UNIQUE,  -- Normalized party name
  nombre_corto TEXT,   -- Short name
  color TEXT           -- Hex color for visualization
)

resultados (
  id INTEGER PRIMARY KEY,
  anio INTEGER,
  cargo TEXT,
  seccional_id INTEGER → seccionales(id),
  agrupacion_id INTEGER → agrupaciones(id),
  votos INTEGER
)
```

## Political Context

### Major Political Forces (Agrupaciones)

**Evolution observed:**
- **LA LIBERTAD AVANZA**: Explosive growth from 17k (2021) → 266k (2023)
- **JUNTOS POR EL CAMBIO**: Decline from 406k (2021) → 195k (2023)
- **HACEMOS POR CÓRDOBA**: Stable ~250k votes
- **UNIÓN POR LA PATRIA**: ~60k-96k votes

When analyzing trends, focus on:
- **Volatilidad electoral** (Pedersen Index): Measures vote swing between elections
- **Seccionales competitivas**: Areas with tight races (small margin between 1st/2nd place)
- **Spatial patterns**: Do neighboring seccionales vote similarly?

## File Structure Context

### Source Code Organization (`src/`)

**`etl/`**: Data extraction, transformation, and loading
- `extract.py`: Read Excel/GeoJSON with correct encodings (latin-1 for 2021)
- `transform.py`: Apply normalization mappings, filter invalid records
- `load.py`: Write to SQLite database
- `utils.py`: Mapping dictionaries and helper functions

**`analysis/`**: Political science analysis
- `electoral_trends.py`: Time series analysis, vote evolution
- `political_analysis.py`: Volatility, competitiveness, clustering
- `statistics.py`: Descriptive stats, aggregations

**`visualization/`**: Interactive maps and charts
- `maps.py`: Folium choropleth maps (main visualization method)
- `charts.py`: Plotly line/bar/heatmap charts
- `dashboard.py`: Integrated dashboard (Dash or Streamlit)

### Notebooks (`notebooks/`)
Sequential analysis workflow:
1. `01_exploratory_analysis.ipynb`: Initial data inspection
2. `02_data_cleaning.ipynb`: ETL development and validation
3. `03_electoral_evolution.ipynb`: Temporal analysis
4. `04_political_insights.ipynb`: Politological insights

## Visualization Guidelines

### Choropleth Maps (Primary Visualization)
- Use **Folium** for interactive web maps (Leaflet.js backend)
- Base location: `[-31.4201, -64.1888]` (Córdoba coordinates)
- Zoom level: 12 (city-level view)
- Color scheme: `YlOrRd` or `RdYlGn_r` for vote percentages

### Party Colors
Define in `data/mappings/party_colors.json`:
- LA LIBERTAD AVANZA: Purple (#6A0DAD)
- JUNTOS POR EL CAMBIO: Yellow (#FFD700)
- HACEMOS POR CÓRDOBA: Light blue (#87CEEB)
- UNIÓN POR LA PATRIA: Blue (#0047AB)
- FRENTE DE IZQUIERDA: Red (#DC143C)

### Chart Types
- **Line charts**: Vote evolution over time (2021→2023→2025)
- **Stacked bars**: Party composition by seccional
- **Heatmap**: Vote change matrices (2021→2023, 2023→2025)
- **Scatter plots**: Cross-seccional correlations

## Common Workflows

### Adding a New Election Year
1. Add Excel file to `data/raw/`
2. Update `SECCIONAL_MAPPING` in `src/etl/utils.py` if naming changed
3. Run ETL pipeline
4. Verify data in `data/processed/electoral_data_clean.csv`
5. Update visualization year selectors

### Generating a Map
```python
from src.visualization.maps import create_choropleth_map

# Create map for specific year and party
map = create_choropleth_map(
    year=2023,
    agrupacion='LA LIBERTAD AVANZA',
    metric='porcentaje'  # or 'votos'
)

map.save('outputs/maps/lla_2023.html')
```

### Running Analysis
```python
from src.analysis.electoral_trends import calculate_volatility

# Calculate Pedersen volatility index
volatility = calculate_volatility(year_from=2021, year_to=2023)
print(f"Electoral volatility: {volatility:.2f}%")
```

## Dependencies

Core libraries (see `requirements.txt`):
- **pandas**: Data manipulation
- **geopandas**: Geospatial operations
- **folium**: Interactive maps
- **plotly**: Interactive charts
- **openpyxl/xlrd**: Excel file reading
- **sqlite3**: Database (stdlib)
- **jupyter**: Notebooks
- **pytest**: Testing

Optional:
- **dash**: Full dashboard framework
- **scikit-learn**: Advanced clustering analysis
- **statsmodels**: Statistical modeling

## Data Validation Checklist

When working with electoral data, always verify:
- [ ] All 14 seccionales present in each year
- [ ] No duplicate records (anio + seccional + agrupacion should be unique)
- [ ] Vote counts are positive integers
- [ ] Seccional names normalized correctly
- [ ] GeoJSON dissolves to exactly 14 polygons
- [ ] Total votes per seccional/year match official sources
- [ ] Special records (totals) filtered out

## Known Issues & Solutions

**Issue**: Excel encoding errors when reading files
**Solution**: Column names may show as "a�o" instead of "año" - this is handled automatically by `normalize_columns()`

**Issue**: GeoJSON has 120 features but we need 14 seccionales
**Solution**: Use `geopandas.dissolve(by='Seccional')` to aggregate circuits into 14 seccionales

**Issue**: Different number of records per year (2021=98, 2023=70, 2025=252)
**Solution**: This is expected - different parties participated in each election, and 2025 has more granular party data

**Issue**: Data files must be in `data/raw/` directory
**Solution**: Always ensure updated data files are copied to `data/raw/` before running ETL

## Performance Considerations

- GeoJSON simplification: If map rendering is slow, use `geopandas.simplify(tolerance=0.001)`
- Database indexing: Ensure indexes on `(anio)`, `(seccional_id)`, `(agrupacion_id)`
- Caching: Cache processed data in SQLite to avoid re-running ETL
- Notebook outputs: Clear outputs before committing to git

## References

See `PLAN_PROYECTO.md` for:
- Detailed ETL pipeline design
- Complete database schema
- Phase-by-phase implementation plan
- GitHub projects for inspiration
- Political analysis methodologies
