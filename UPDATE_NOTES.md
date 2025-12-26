# Update Notes - Data Normalization

## Date: December 24, 2025

### Changes Made

The source data files have been updated to use normalized column names:

#### 1. **Seccional Column**
- **Old**: Varied names ("Seccinal 1", "SECC PRIMERA", etc.)
- **New**: Standardized as "Seccional 1", "Seccional 2", ..., "Seccional 14"
- All three files (2021, 2023, 2025) now use the same format

#### 2. **Votes Column**
- **Old**: Different names per year
  - 2021: "sum_diputados"
  - 2023: "votos"
  - 2025: "votos"
- **New**: Standardized as "diputados" in all three files

### Updated Files

1. **2021_porseccional_diputados.xls**
   - Columns: año, cargo, seccional, agrupacion, diputados
   - Seccional values: "Seccional 1" through "Seccional 14"

2. **2023_porseccional_diputados.xlsx**
   - Columns: año, cargo, seccional, agrupacion, diputados
   - Seccional values: "Seccional 1" through "Seccional 14"

3. **2025_porseccional_diputados.xlsx**
   - Columns: año, cargo, Seccional, agrupacion, diputados
   - Seccional values: "Seccional 1" through "Seccional 14"
   - Note: Column name is "Seccional" (capital S) but values are same format

### Code Updates

The ETL pipeline was updated to handle the normalized data:

1. **`data/mappings/seccional_names.json`**
   - Simplified to map only "Seccional 1" → "1", etc.
   - Removed old variations (SECC PRIMERA, Seccinal, etc.)

2. **`src/etl/utils.py`**
   - Updated `COLUMN_MAPPING` to include:
     - "diputados" → "votos"
     - "Seccional" → "seccional" (for 2025 capital S)
   - Updated `normalize_columns()` to handle "diputados" column

### ETL Results

After processing the normalized data:
- **Total records**: 420 ✅
- **Years**: 2021, 2023, 2025 ✅
- **Seccionales**: 14 (numbered 1-14) ✅
- **Political parties**: 24 ✅
- **No filtered records** (all data valid) ✅

### Data Quality Improvements

✅ **No more inconsistent seccional names**
✅ **Uniform column names across years**
✅ **Easier to maintain and update**
✅ **Better data integrity**

### How to Use

1. **If data files are updated in the future**:
   - Place them in the project root or directly in `data/raw/`
   - Run: `python -m src.etl`
   - Data will be automatically processed

2. **Expected data format**:
   ```
   año, cargo, seccional, agrupacion, diputados
   2021, DIPUTADOS NACIONALES, Seccional 1, JUNTOS POR EL CAMBIO, 5904
   ```

3. **Seccional values must be**:
   - "Seccional 1", "Seccional 2", ..., "Seccional 14"
   - Exactly this format (case-sensitive)

### Files Location

**Source files** should be in:
- `data/raw/2021_porseccional_diputados.xls`
- `data/raw/2023_porseccional_diputados.xlsx`
- `data/raw/2025_porseccional_diputados.xlsx`

**Processed files** will be created in:
- `data/processed/electoral_data_clean.csv`
- `data/processed/seccionales_geo.geojson`
- `data/processed/electoral_database.db`

### Verification

To verify the data after ETL:

```bash
python -c "import pandas as pd; df = pd.read_csv('data/processed/electoral_data_clean.csv'); print(f'Records: {len(df)}'); print(f'Years: {sorted(df[\"anio\"].unique())}'); print(f'Seccionales: {len(df[\"seccional\"].unique())}')"
```

Expected output:
```
Records: 420
Years: [2021, 2023, 2025]
Seccionales: 14
```

---

## Migration from Old Format

If you have old data files with the previous format, they can still be processed by updating the mapping file, but it's recommended to use the new normalized format for consistency.

### Old Format (deprecated):
- 2021: "Seccinal 1" (typo), "sum_diputados"
- 2023: Mix of "Seccinal" and "Seccional", "votos"
- 2025: "SECC PRIMERA", "votos"

### New Format (current):
- All years: "Seccional 1", "diputados"

---

**Status**: ✅ System updated and tested with normalized data
**Next run**: Just execute `run.bat` or `python app.py`
