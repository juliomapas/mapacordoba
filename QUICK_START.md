# Quick Start Guide

## Installation & Setup

### Option 1: Using Batch Files (Windows - Recommended)

1. **Initial Setup** (run once):
   ```cmd
   setup.bat
   ```
   This will create a virtual environment and install all dependencies.

2. **Run the Dashboard**:
   ```cmd
   run.bat
   ```
   This will automatically process data (if needed) and start the dashboard.

3. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:8050
   ```

### Option 2: Manual Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Process data** (first time only):
   ```bash
   python -m src.etl
   ```

5. **Start dashboard**:
   ```bash
   python app.py
   ```

6. **Open browser** at `http://127.0.0.1:8050`

## Features

### Maps Tab
- **Interactive choropleth maps** showing vote distribution
- Filter by year (2021, 2023, 2025) and political party
- View percentages or absolute vote counts
- Winner table by seccional

### Trends Tab
- **Vote evolution over time** (line charts)
- **Growth rate analysis** between election periods
- **Vote distribution** by seccional
- Compare multiple parties side-by-side

### Analysis Tab
- **Pedersen Volatility Index**: Measures electoral volatility between elections
- **Competitive Seccionales**: Identifies close races (margin < 5%)
- **Electoral Concentration (HHI)**: Shows vote concentration per seccional
- **Flipped Seccionales**: Tracks changes in winning party

### About Tab
- Project information
- Data sources
- Technology stack

## Responsive Design

The dashboard is fully responsive and works on:
- **Desktop** (1920x1080 and above)
- **Tablets** (768px-1024px)
- **Mobile** (320px-767px)

## Troubleshooting

### Module not found errors
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### No data errors
- Run `python -m src.etl` to process the data first

### Port already in use
- Change the port in `app.py`:
  ```python
  app.run_server(debug=True, host='0.0.0.0', port=8051)  # Use different port
  ```

## Project Structure

```
pyoclaude/
├── app.py                  # Main dashboard application
├── setup.bat               # Windows setup script
├── run.bat                 # Windows run script
├── data/
│   ├── raw/                # Original data files
│   └── processed/          # Processed data (after ETL)
├── src/
│   ├── etl/                # Data processing pipeline
│   ├── analysis/           # Analysis modules
│   ├── visualization/      # Visualization components
│   └── config/             # Configuration
└── outputs/                # Generated maps and reports
```

## Next Steps

After exploring the dashboard, you can:

1. **Customize colors**: Edit `data/mappings/party_colors.json`
2. **Add more analysis**: Create new modules in `src/analysis/`
3. **Export data**: Use the processed CSV in `data/processed/`
4. **Generate reports**: Add export functionality to the dashboard

## Support

For issues or questions, check:
- `CLAUDE.md` - Technical documentation
- `PLAN_PROYECTO.md` - Detailed project plan
- `README.md` - Full project documentation
