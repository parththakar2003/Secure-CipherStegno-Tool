#!/bin/bash
# Setup script for Secure CipherStegno Tool
# This script creates a virtual environment and installs dependencies

set -e  # Exit on error

echo "=================================================="
echo "Secure CipherStegno Tool - Setup Script"
echo "=================================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
if [ ! -f "check_python.py" ]; then
    echo "❌ Error: check_python.py not found"
    echo "Please make sure you're in the Secure-CipherStegno-Tool directory"
    exit 1
fi

python3 check_python.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Python version check failed"
    exit 1
fi

echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✓ Virtual environment created successfully"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=================================================="
echo "✓ Setup completed successfully!"
echo "=================================================="
echo ""
echo "To use the tool:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Choose your interface:"
echo ""
echo "     📱 Unified Launcher (Recommended):"
echo "        python launch.py gui           # GUI interface"
echo "        python launch.py interactive   # Interactive CLI"
echo "        python launch.py web           # Web interface"
echo "        python launch.py cli --help    # Command-line"
echo ""
echo "     🖥️  Direct Interface Launch:"
echo "        python app.py                  # GUI application"
echo "        python interactive_cli.py      # Interactive CLI"
echo "        python cli.py --help           # Command-line"
echo "        python src/web/api.py          # Web server"
echo ""
echo "  3. When done, deactivate the virtual environment:"
echo "     deactivate"
echo "=================================================="
