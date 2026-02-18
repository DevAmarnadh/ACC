@echo off
echo ========================================
echo   AI Content Creation Engine
echo   Starting Streamlit Application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Check if installation was successful
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Trying without quiet mode...
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Starting Streamlit Server...
echo ========================================
echo.
echo   Application will open in your browser
echo   URL: http://localhost:8501
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the Streamlit application
streamlit run app.py

pause
