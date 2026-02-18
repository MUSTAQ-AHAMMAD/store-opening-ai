#!/bin/bash

# Store Opening AI - Start Backend Script
# Activates virtual environment and starts the backend API

set -e

echo "============================================================"
echo "Starting Store Opening AI Backend..."
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

# Check if database exists
if [ ! -f "store_opening.db" ]; then
    echo "⚠️  Warning: Database not found. Initializing..."
    python data/seed_beta_data.py
    echo ""
fi

# Start backend
echo "Starting backend on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python main.py
