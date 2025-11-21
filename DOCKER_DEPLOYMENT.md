# Docker Deployment Guide for Manajet

Deploy your Manajet application using Docker in minutes!

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) installed (1.29+)

## Quick Start (2 Minutes)

### 1. Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output.

### 2. Create Environment File

```bash
# Copy the template
cp .env.docker .env

# Edit .env and paste your secret key
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
```

Replace `your-secret-key-here-change-in-production` with your generated secret key.

### 3. Deploy with Docker Compose

```bash
docker-compose up -d
```

That's it! Your app is now running at **http://localhost:5000**

---

## Detailed Instructions

### Build the Docker Image

```bash
# Build the image
docker build -t manajet-app .

# Or use docker-compose to build
docker-compose build
```

### Run with Docker Compose (Recommended)

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Run with Docker Directly

```bash
# Run the container
docker run -d \
  --name manajet \
  -p 5000:5000 \
  -e SECRET_KEY="your-secret-key-here" \
  -e DEBUG=False \
  -v $(pwd)/jet_schedule_data.json:/app/jet_schedule_data.json \
  manajet-app

# View logs
docker logs -f manajet

# Stop the container
docker stop manajet

# Remove the container
docker rm manajet
```

---

## Environment Variables

Set these in your `.env` file or pass them via `-e` flag:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | **Yes** | - | Flask session secret (use `secrets.token_hex(32)`) |
| `DEBUG` | No | `False` | Enable debug mode (use `False` in production) |
| `PORT` | No | `5000` | Port to run the application |
| `SESSION_COOKIE_SECURE` | No | `False` | Set to `True` if using HTTPS |
| `PERMANENT_SESSION_LIFETIME` | No | `3600` | Session timeout in seconds |

---

## Data Persistence

### Using Docker Volumes

Your data is automatically persisted in `jet_schedule_data.json`. The docker-compose configuration mounts this file.

**Backup your data:**
```bash
# Copy from container
docker cp manajet:/app/jet_schedule_data.json ./backup_$(date +%Y%m%d).json

# Or just copy the local file
cp jet_schedule_data.json backup_$(date +%Y%m%d).json
```

**Restore data:**
```bash
# Stop the container
docker-compose down

# Restore the backup
cp backup_20231120.json jet_schedule_data.json

# Start again
docker-compose up -d
```

### Initialize Sample Data

```bash
# Run setup script in container
docker-compose exec manajet python setup_initial_data.py

# Or if using docker run:
docker exec -it manajet python setup_initial_data.py
```

---

## Default Login Credentials

After initializing sample data:

**Admin:**
- Username: `admin`
- Password: `admin123`

**Customer:**
- Username: `johnsmith`
- Password: `customer123`

**Crew:**
- Username: `pilot_mike`
- Password: `crew123`

**Mechanic:**
- Username: `mechanic_joe`
- Password: `mech123`

⚠️ **IMPORTANT:** Change these passwords after first login!

---

## Production Deployment

### 1. Use HTTPS (Recommended)

Add Nginx reverse proxy with SSL:

```yaml
# Uncomment nginx service in docker-compose.yml
# Create nginx.conf with SSL configuration
# Add SSL certificates to ./ssl directory
```

Example `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream manajet {
        server manajet:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://manajet;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Then update `.env`:
```
SESSION_COOKIE_SECURE=True
```

### 2. Secure Your Environment Variables

```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Use strong secret key
python -c "import secrets; print(secrets.token_hex(64))"

# Set restrictive permissions
chmod 600 .env
```

### 3. Monitor Your Application

```bash
# View real-time logs
docker-compose logs -f manajet

# Check container health
docker-compose ps

# View resource usage
docker stats manajet
```

### 4. Automatic Restarts

The docker-compose.yml is configured with `restart: unless-stopped`, so your container will automatically restart on failures or system reboots.

---

## Updating the Application

```bash
# 1. Pull latest code
git pull origin master

# 2. Rebuild the image
docker-compose build

# 3. Restart with new image
docker-compose up -d

# 4. Verify it's running
docker-compose ps
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs manajet

# Common issues:
# - Missing SECRET_KEY: Set in .env file
# - Port already in use: Change port in docker-compose.yml
# - Permission denied: Run with sudo or add user to docker group
```

### Can't access the application

```bash
# Check if container is running
docker-compose ps

# Check port binding
docker port manajet

# Test locally in container
docker-compose exec manajet curl http://localhost:5000/login
```

### Data not persisting

```bash
# Check volume mounts
docker-compose config

# Ensure jet_schedule_data.json exists
touch jet_schedule_data.json

# Restart
docker-compose restart
```

### Reset everything

```bash
# Stop and remove containers, networks, volumes
docker-compose down -v

# Remove images
docker rmi manajet-app

# Start fresh
docker-compose up -d
```

---

## Advanced Configuration

### Using PostgreSQL Instead of JSON

1. Add PostgreSQL service to `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: manajet
      POSTGRES_USER: manajet
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

2. Update `jet_manager.py` to use PostgreSQL
3. Set `DATABASE_URL` environment variable

### Scaling with Multiple Workers

```bash
# Scale to 3 instances
docker-compose up -d --scale manajet=3

# Add load balancer (nginx) in front
```

### Custom Port

Edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Access on port 8080
```

---

## Health Checks

The container includes health checks that run every 30 seconds:

```bash
# View health status
docker inspect --format='{{.State.Health.Status}}' manajet

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' manajet
```

---

## Docker Hub Deployment (Optional)

### Push to Docker Hub

```bash
# Tag the image
docker tag manajet-app yourusername/manajet:latest

# Login to Docker Hub
docker login

# Push
docker push yourusername/manajet:latest
```

### Deploy from Docker Hub

```bash
# Pull and run
docker pull yourusername/manajet:latest
docker run -d -p 5000:5000 \
  -e SECRET_KEY="your-key" \
  yourusername/manajet:latest
```

---

## Cloud Deployment

### Deploy to AWS ECS

```bash
# Use AWS Copilot CLI
copilot init --app manajet --name web --type "Load Balanced Web Service" --dockerfile ./Dockerfile
copilot deploy
```

### Deploy to Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/manajet
gcloud run deploy manajet --image gcr.io/PROJECT-ID/manajet --platform managed
```

### Deploy to Azure Container Instances

```bash
# Create container instance
az container create \
  --resource-group myResourceGroup \
  --name manajet \
  --image manajet-app \
  --ports 5000
```

---

## Support

- Check logs: `docker-compose logs -f`
- Docker documentation: https://docs.docker.com/
- Docker Compose documentation: https://docs.docker.com/compose/

---

**Your Manajet app is now Dockerized and ready to deploy anywhere! 🐳**
