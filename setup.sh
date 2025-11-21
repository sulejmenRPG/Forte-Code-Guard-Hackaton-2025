#!/bin/bash

echo "========================================"
echo "AI Code Review Assistant - Setup"
echo "========================================"
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Please make sure Python 3.11+ is installed"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/4] Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created! Please edit it with your credentials."
else
    echo ".env file already exists."
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: ./run.sh"
echo ""
