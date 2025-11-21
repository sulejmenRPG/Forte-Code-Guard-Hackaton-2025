@echo off
echo Starting AI Code Review Assistant...
echo.

cd backend

if not exist "..\venv" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    exit /b 1
)

call ..\venv\Scripts\activate

echo Checking .env file...
if not exist "..\\.env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and fill in your credentials
    pause
    exit /b 1
)

echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python main.py
