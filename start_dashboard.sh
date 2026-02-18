#!/bin/bash

# Store Opening AI - Start React Dashboard Script
# Starts the React.js frontend dashboard

set -e

echo "============================================================"
echo "Starting Store Opening AI React Dashboard..."
echo "============================================================"
echo ""

# Check if react-frontend directory exists
if [ ! -d "react-frontend" ]; then
    echo "❌ Error: react-frontend directory not found."
    exit 1
fi

# Navigate to react-frontend directory
cd react-frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing React dependencies..."
    npm install
    echo ""
fi

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

# Start React dashboard
echo "Starting React dashboard..."
echo "Dashboard will open at http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""
npm start
