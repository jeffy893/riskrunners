@echo off
REM Enhanced Responsibility Futures Analysis Runner for Windows
REM Generates HTML reports and PNG visualizations from Cortext.io data

echo 🚀 Responsibility Futures Enhanced Analysis
echo ==========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed
    echo Please install Python 3 and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import pandas, matplotlib, seaborn, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Some required packages are missing
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Change to src directory
cd src

REM Run the enhanced workflow
echo 🔬 Starting analysis workflow...
python enhanced_workflow.py %*

echo.
echo 📁 Check the 'output' directory for generated reports and visualizations
echo 🌐 Open the HTML file in your browser to view the complete analysis
pause