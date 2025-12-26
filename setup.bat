@echo off
echo ============================================================
echo Electoral Evolution - Setup
echo ============================================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/3] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo To run the application:
echo   1. venv\Scripts\activate
echo   2. python -m src.etl  (first time only, to process data)
echo   3. python app.py
echo.
pause
