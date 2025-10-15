@echo off
echo ========================================
echo Private Jet Manager - Web Setup
echo ========================================
echo.

echo Step 1/3: Generating HTML templates...
python generate_templates.py
echo.

echo Step 2/3: Installing Flask...
pip install flask gunicorn
echo.

echo Step 3/3: Starting web server...
echo.
echo ========================================
echo Web app is starting!
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python web_app.py
