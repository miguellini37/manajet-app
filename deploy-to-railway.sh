#!/bin/bash

echo "========================================"
echo "  Manajet Railway Deployment Script"
echo "========================================"
echo ""

echo "Step 1: Logging into Railway..."
railway login
if [ $? -ne 0 ]; then
    echo "Failed to login. Please try again."
    exit 1
fi
echo "Login successful!"
echo ""

echo "Step 2: Initializing Railway project..."
railway init
if [ $? -ne 0 ]; then
    echo "Failed to initialize project."
    exit 1
fi
echo "Project initialized!"
echo ""

echo "Step 3: Generating secure SECRET_KEY..."
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
echo "SECRET_KEY generated: $SECRET_KEY"
echo ""

echo "Step 4: Setting environment variables..."
railway variables set SECRET_KEY="$SECRET_KEY"
railway variables set DEBUG="False"
railway variables set SESSION_COOKIE_SECURE="True"
railway variables set PERMANENT_SESSION_LIFETIME="3600"
echo "Environment variables set!"
echo ""

echo "Step 5: Deploying application to Railway..."
railway up
if [ $? -ne 0 ]; then
    echo "Deployment failed. Check the errors above."
    exit 1
fi
echo ""

echo "========================================"
echo "  Deployment Complete!"
echo "========================================"
echo ""
echo "Your application is being built and deployed."
echo ""
echo "To get your application URL, run:"
echo "  railway domain"
echo ""
echo "To view logs:"
echo "  railway logs"
echo ""
