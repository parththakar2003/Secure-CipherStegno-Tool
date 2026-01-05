@echo off
REM Setup script for Secure CipherStegno Tool (Windows)
REM This script creates a virtual environment and installs dependencies

echo ==================================================
echo Secure CipherStegno Tool - Setup Script
echo ==================================================
echo.

REM Check if Python 3 is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: python is not installed
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    exit /b 1
)

REM Check Python version
echo Checking Python version...
if not exist check_python.py (
    echo Error: check_python.py not found
    echo Please make sure you're in the Secure-CipherStegno-Tool directory
    exit /b 1
)

python check_python.py
if errorlevel 1 (
    echo.
    echo Python version check failed
    exit /b 1
)

echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo Virtual environment created successfully
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ==================================================
echo Setup completed successfully!
echo ==================================================
echo.
echo To use the tool:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Run the GUI application:
echo      python app.py
echo.
echo   3. Or use the CLI:
echo      python cli.py --help
echo.
echo   4. When done, deactivate the virtual environment:
echo      deactivate
echo ==================================================
pause
