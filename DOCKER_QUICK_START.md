# Docker Quick Start - 2 Minutes to Deploy!

## Prerequisites
- Docker installed ([Get Docker](https://www.docker.com/get-started))
- Docker Compose installed

## Deploy in 3 Steps

### 1. Run the deployment script

**Windows:**
```cmd
docker-deploy.bat
```

**Mac/Linux:**
```bash
./docker-deploy.sh
```

### 2. Initialize sample data

```bash
docker-compose exec manajet python setup_initial_data.py
```

### 3. Access your app

Open your browser to: **http://localhost:5000**

Login with:
- Username: `admin`
- Password: `admin123`

---

## That's it! 🎉

Your Manajet app is now running in Docker!

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop the app
docker-compose down

# Restart the app
docker-compose restart

# Check status
docker-compose ps
```

## Full Documentation

For detailed instructions, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
