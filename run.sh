#!/bin/bash

echo "Starting AI Code Review Assistant..."
echo ""

cd backend

if [ ! -d "../venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

source ../venv/bin/activate

echo "Checking .env file..."
if [ ! -f "../.env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and fill in your credentials"
    exit 1
fi

echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python main.py
