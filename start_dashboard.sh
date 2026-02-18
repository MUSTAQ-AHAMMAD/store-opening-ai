#!/bin/bash

# Store Opening AI - Start Dashboard Script
# Activates virtual environment and starts the Streamlit dashboard

set -e

echo "============================================================"
echo "Starting Store Opening AI Dashboard..."
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found."
    echo "   Please run ./setup.sh first to set up the project."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if backend is running
echo "Checking if backend is running..."
if ! curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "⚠️  Warning: Backend might not be running."
    echo "   Make sure to start the backend first:"
    echo "   ./start_backend.sh (in another terminal)"
    echo ""
    echo "Continuing anyway..."
    echo ""
fi

# Start dashboard
echo "Starting dashboard (will open in browser)..."
echo "Press Ctrl+C to stop"
echo ""
streamlit run frontend/dashboard.py
