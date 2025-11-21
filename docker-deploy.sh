#!/bin/bash

echo "========================================"
echo "  Manajet Docker Deployment Script"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker is installed"
echo "✅ Docker Compose is installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.docker .env

    echo ""
    echo "🔐 Generating secure SECRET_KEY..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || python -c "import secrets; print(secrets.token_hex(32))")

    # Replace SECRET_KEY in .env file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
    fi

    echo "✅ .env file created with secure SECRET_KEY"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🐳 Building Docker image..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed. Please check the errors above."
    exit 1
fi

echo ""
echo "✅ Docker image built successfully"
echo ""

# Check if data file exists
if [ ! -f jet_schedule_data.json ]; then
    echo "📊 No data file found. Creating empty data file..."
    echo "{}" > jet_schedule_data.json
    echo "✅ Empty data file created"
    echo ""
    echo "💡 You can initialize sample data after deployment with:"
    echo "   docker-compose exec manajet python setup_initial_data.py"
fi

echo ""
echo "🚀 Starting Manajet application..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start application. Please check the errors above."
    exit 1
fi

echo ""
echo "========================================"
echo "  ✅ Deployment Complete!"
echo "========================================"
echo ""
echo "📱 Your Manajet app is now running at:"
echo "   http://localhost:5000"
echo ""
echo "📋 Useful commands:"
echo "   View logs:        docker-compose logs -f"
echo "   Stop app:         docker-compose down"
echo "   Restart app:      docker-compose restart"
echo "   Check status:     docker-compose ps"
echo ""
echo "🔑 Default login (after initializing sample data):"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📚 For more information, see DOCKER_DEPLOYMENT.md"
echo ""
