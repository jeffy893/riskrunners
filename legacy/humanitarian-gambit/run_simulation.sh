#!/bin/bash

echo "🎯 Humanitarian Gambit Simulation Setup"
echo "========================================"

# Check if Python 3.10 is available
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Python 3 not found. Please install Python 3.10 or later."
    exit 1
fi

echo "✅ Using Python: $PYTHON_CMD"

# Install requirements
echo "📦 Installing requirements..."
$PYTHON_CMD -m pip install -r requirements.txt

# Run simulation
echo "🚀 Running simulation..."
$PYTHON_CMD simulation.py

echo "🎉 Simulation complete! Check simulation_results.png for visualizations."