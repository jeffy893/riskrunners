#!/bin/bash
# Enhanced Responsibility Futures Analysis Runner
# Generates HTML reports and PNG visualizations from Cortext.io data

echo "🚀 Responsibility Futures Enhanced Analysis"
echo "=========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import pandas, matplotlib, seaborn, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some required packages are missing"
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Change to src directory
cd src

# Run the enhanced workflow
echo "🔬 Starting analysis workflow..."
python3 enhanced_workflow.py "$@"

echo ""
echo "📁 Check the 'output' directory for generated reports and visualizations"
echo "🌐 Open the HTML file in your browser to view the complete analysis"