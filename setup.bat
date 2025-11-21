@echo off
echo ========================================
echo AI Code Review Assistant - Setup
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Please make sure Python 3.11+ is installed
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo .env file created! Please edit it with your credentials.
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: run.bat
echo.
pause
