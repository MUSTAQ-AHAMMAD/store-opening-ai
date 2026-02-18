#!/bin/bash

# Store Opening AI - Quick Setup Script
# This script automates the initial setup process

set -e  # Exit on error

echo "============================================================"
echo "Store Opening AI - Quick Setup Script"
echo "============================================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check if Python version is >= 3.9
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "❌ Error: Python 3.9 or higher is required."
    echo "   Your version: $PYTHON_VERSION"
    echo "   Please install Python 3.9+ and try again."
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Check Node.js version
echo "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "⚠️  Warning: Node.js not found."
    echo "   Node.js is required for the React frontend."
    echo "   Please install Node.js 14+ from https://nodejs.org/"
    echo ""
else
    NODE_VERSION=$(node --version)
    echo "Found Node.js $NODE_VERSION"
    echo "✅ Node.js version OK"
    echo ""
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
echo "✅ Python dependencies installed"
echo ""

# Install React frontend dependencies
if command -v npm &> /dev/null; then
    echo "Installing React frontend dependencies..."
    cd react-frontend
    npm install
    cd ..
    echo "✅ React frontend dependencies installed"
    echo ""
else
    echo "⚠️  Skipping React frontend setup (Node.js not found)"
    echo ""
fi

# Setup .env file
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    
    # Set TEST_MODE=true by default
    sed -i 's/TEST_MODE=false/TEST_MODE=true/' .env 2>/dev/null || sed -i '' 's/TEST_MODE=false/TEST_MODE=true/' .env
    
    echo "✅ .env file created with TEST_MODE enabled"
else
    echo "✅ .env file already exists (not modified)"
fi
echo ""

# Initialize database
echo "Initializing database with sample data..."
python data/seed_beta_data.py
echo "✅ Database initialized"
echo ""

echo "============================================================"
echo "Setup Complete! 🎉"
echo "============================================================"
echo ""
echo "You can now start the application:"
echo ""
echo "  Terminal 1 - Backend API:"
echo "    source venv/bin/activate"
echo "    python main.py"
echo ""
echo "  Terminal 2 - React Dashboard:"
echo "    ./start_dashboard.sh"
echo ""
echo "Then open your browser to:"
echo "  - Backend: http://localhost:5000"
echo "  - React Dashboard: http://localhost:3000"
echo ""
echo "Login with:"
echo "  - Username: admin"
echo "  - Password: admin123"
echo ""
echo "For more details, see REACT_QUICKSTART.md"
echo "============================================================"
