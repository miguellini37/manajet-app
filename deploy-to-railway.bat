@echo off
echo ========================================
echo   Manajet Railway Deployment Script
echo ========================================
echo.

echo Step 1: Logging into Railway...
call railway login
if errorlevel 1 (
    echo Failed to login. Please try again.
    pause
    exit /b 1
)
echo Login successful!
echo.

echo Step 2: Initializing Railway project...
call railway init
if errorlevel 1 (
    echo Failed to initialize project.
    pause
    exit /b 1
)
echo Project initialized!
echo.

echo Step 3: Generating secure SECRET_KEY...
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY=%%i
echo SECRET_KEY generated: %SECRET_KEY%
echo.

echo Step 4: Setting environment variables...
call railway variables set SECRET_KEY="%SECRET_KEY%"
call railway variables set DEBUG="False"
call railway variables set SESSION_COOKIE_SECURE="True"
call railway variables set PERMANENT_SESSION_LIFETIME="3600"
echo Environment variables set!
echo.

echo Step 5: Deploying application to Railway...
call railway up
if errorlevel 1 (
    echo Deployment failed. Check the errors above.
    pause
    exit /b 1
)
echo.

echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Your application is being built and deployed.
echo.
echo To get your application URL, run:
echo   railway domain
echo.
echo To view logs:
echo   railway logs
echo.
pause
