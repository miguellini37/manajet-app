@echo off
echo ========================================
echo   Manajet Docker Deployment Script
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo X Docker is not installed. Please install Docker Desktop first.
    echo   Visit: https://www.docker.com/get-started
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo X Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [OK] Docker is installed
echo [OK] Docker Compose is installed
echo.

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.docker .env >nul

    echo.
    echo Generating secure SECRET_KEY...
    for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY=%%i

    REM Replace SECRET_KEY in .env file
    powershell -Command "(gc .env) -replace 'your-secret-key-here-change-in-production', '%SECRET_KEY%' | Out-File -encoding ASCII .env"

    echo [OK] .env file created with secure SECRET_KEY
) else (
    echo [OK] .env file already exists
)

echo.
echo Building Docker image...
docker-compose build

if errorlevel 1 (
    echo X Docker build failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo [OK] Docker image built successfully
echo.

REM Check if data file exists
if not exist jet_schedule_data.json (
    echo No data file found. Creating empty data file...
    echo {} > jet_schedule_data.json
    echo [OK] Empty data file created
    echo.
    echo You can initialize sample data after deployment with:
    echo   docker-compose exec manajet python setup_initial_data.py
)

echo.
echo Starting Manajet application...
docker-compose up -d

if errorlevel 1 (
    echo X Failed to start application. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [OK] Deployment Complete!
echo ========================================
echo.
echo Your Manajet app is now running at:
echo   http://localhost:5000
echo.
echo Useful commands:
echo   View logs:        docker-compose logs -f
echo   Stop app:         docker-compose down
echo   Restart app:      docker-compose restart
echo   Check status:     docker-compose ps
echo.
echo Default login (after initializing sample data):
echo   Username: admin
echo   Password: admin123
echo.
echo For more information, see DOCKER_DEPLOYMENT.md
echo.
pause
