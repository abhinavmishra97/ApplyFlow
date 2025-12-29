@echo off
echo ========================================
echo ApplyFlow - Quick Start Script
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo Checking if virtual environment exists...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing/Updating dependencies...
pip install -r requirements.txt
echo.

echo Checking PostgreSQL connection...
psql -U postgres -c "SELECT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Cannot connect to PostgreSQL
    echo Please ensure PostgreSQL is installed and running
    echo.
)

echo Checking Redis connection...
redis-cli ping >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Cannot connect to Redis
    echo Please ensure Redis is installed and running
    echo.
)

echo Checking .env file...
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your configuration!
    echo.
) else (
    echo .env file exists.
)
echo.

echo Checking uploads directory...
if not exist "uploads\" (
    mkdir uploads
    echo Created uploads directory.
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Download Gmail API credentials.json from Google Cloud Console
echo 3. Run: python init_db.py (to create database tables)
echo 4. Run: python run.py (to start Flask server)
echo 5. In another terminal, run: celery -A celery_worker.celery worker --loglevel=info --pool=solo
echo.
pause
