@echo off
echo ============================================================
echo Electoral Evolution Dashboard - Startup
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if data is processed
if not exist "data\processed\electoral_data_clean.csv" (
    echo [INFO] Processed data not found. Running ETL pipeline...
    python -m src.etl
    if errorlevel 1 (
        echo ERROR: ETL pipeline failed
        pause
        exit /b 1
    )
)

REM Start dashboard
echo.
echo Starting dashboard...
python app.py

pause
