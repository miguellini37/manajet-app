# Private Jet Management System - Web Deployment Guide

This guide covers multiple deployment options from simplest to most enterprise-ready.

---

## Option 1: Flask Web App (RECOMMENDED - Started Above)

### ✅ Pros:
- Minimal changes to existing code
- Easy to develop and test locally
- Can be deployed anywhere Python runs
- Existing business logic works perfectly

### 📦 Quick Setup:

```bash
# Install Flask
pip install flask

# Run the web app
python web_app.py

# Access at: http://localhost:5000
```

### 🚀 Deployment Options for Flask:

#### A. **PythonAnywhere (Easiest - Free tier available)**
- Perfect for small deployments
- No server management
- Free tier: pythonanywhereusername.pythonanywhere.com

**Steps:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via dashboard
3. Install Flask in virtual environment
4. Configure WSGI file
5. Done! Your app is live

**Cost:** Free tier available, paid plans from $5/month

---

#### B. **Heroku (Easy - Great for startups)**

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn web_app:app" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
heroku login
heroku create your-app-name
git push heroku main
```

**Files needed:**
- `Procfile`: `web: gunicorn web_app:app`
- `requirements.txt`: Generated with `pip freeze`
- `runtime.txt`: `python-3.11.0` (specify Python version)

**Cost:** Free tier (with limitations), paid from $7/month

---

#### C. **DigitalOcean App Platform (Balanced)**
- Automatic scaling
- Database integration
- Easy GitHub integration

**Steps:**
1. Connect GitHub repository
2. Select Python as runtime
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn web_app:app`
5. Deploy!

**Cost:** From $5/month

---

#### D. **AWS (EC2 + RDS) (Enterprise-grade)**

Full setup for production:

```bash
# On EC2 instance:
sudo apt update
sudo apt install python3-pip nginx

# Install dependencies
pip3 install flask gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 web_app:app

# Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/jetmanager
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Cost:** From $10/month (EC2 t3.micro + RDS)

---

## Option 2: Django Web App (Better for Complex Features)

### When to choose Django:
- Need user authentication/permissions
- Want admin panel out of the box
- Planning complex features later
- Need built-in security features

### Quick Start:

```bash
# Install Django
pip install django

# Create project
django-admin startproject jetmanager
cd jetmanager
python manage.py startapp core

# Migrate existing models
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Deployment:** Same options as Flask (Heroku, AWS, etc.)

---

## Option 3: FastAPI (Modern, Fast API-first)

### When to choose FastAPI:
- Building a REST API
- Want automatic API documentation
- Planning mobile app integration
- Need high performance

### Quick Start:

```bash
pip install fastapi uvicorn

# Create main.py
from fastapi import FastAPI
from jet_manager import JetScheduleManager

app = FastAPI()
manager = JetScheduleManager()

@app.get("/api/jets")
def get_jets():
    return list(manager.jets.values())

# Run
uvicorn main:app --reload
```

**API Docs automatically at:** `http://localhost:8000/docs`

---

## Option 4: Streamlit (Fastest Prototyping)

### When to choose Streamlit:
- Need something running in 1 hour
- Internal tool (not public-facing)
- Minimal design work wanted

```bash
pip install streamlit

# Create streamlit_app.py
import streamlit as st
from jet_manager import JetScheduleManager

st.title("Private Jet Manager")
manager = JetScheduleManager()

# Show passengers
st.subheader("Passengers")
st.dataframe([(p.name, p.passport_number) for p in manager.passengers.values()])

# Run
streamlit run streamlit_app.py
```

**Deploy to Streamlit Cloud:** Free hosting at share.streamlit.io

---

## Option 5: Full Modern Stack (Most Professional)

### Frontend: React/Vue/Angular
### Backend: FastAPI
### Database: PostgreSQL
### Deployment: Docker + Kubernetes

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "web_app:app", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/jetmanager
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: jetmanager
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Database Upgrades (Important for Production!)

### Current: JSON File Storage
**Good for:** Development, small deployments
**Not good for:** Multiple users, concurrent access

### Upgrade Path:

#### 1. SQLite (Easy upgrade)
```python
import sqlite3

class JetScheduleManager:
    def __init__(self, db_path="jet_schedule.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
```

#### 2. PostgreSQL (Production-ready)
```python
import psycopg2

class JetScheduleManager:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)
```

#### 3. Use an ORM (Recommended)
```python
# With SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost/jetmanager')
Session = sessionmaker(bind=engine)
```

---

## Security Checklist for Production

- [ ] Change Flask secret key
- [ ] Add user authentication (Flask-Login, Auth0, or similar)
- [ ] Use HTTPS (Let's Encrypt for free SSL)
- [ ] Encrypt passport numbers at rest
- [ ] Add rate limiting (Flask-Limiter)
- [ ] Set up CORS properly
- [ ] Use environment variables for secrets
- [ ] Add CSRF protection
- [ ] Implement input validation
- [ ] Set up logging and monitoring
- [ ] Regular backups of database
- [ ] Add API authentication (JWT tokens)

---

## Recommended Stack by Scale

### Small Business (1-10 users)
**Stack:** Flask + SQLite + PythonAnywhere
**Cost:** $5-20/month
**Setup time:** 1-2 days

### Medium Business (10-100 users)
**Stack:** Flask + PostgreSQL + Heroku
**Cost:** $25-100/month
**Setup time:** 3-5 days

### Enterprise (100+ users)
**Stack:** FastAPI + PostgreSQL + AWS/Azure
**Cost:** $100-500/month
**Setup time:** 2-4 weeks

---

## Next Steps

1. **Complete the templates** - I've created base.html and dashboard.html. You need:
   - passengers.html, passenger_form.html, passenger_detail.html
   - jets.html, jet_form.html, jet_detail.html
   - flights.html, flight_form.html, flight_detail.html
   - maintenance.html, maintenance_form.html, maintenance_detail.html

2. **Add authentication** - Use Flask-Login or Auth0

3. **Upgrade database** - Move from JSON to SQLite/PostgreSQL

4. **Add tests** - pytest for backend, Selenium for frontend

5. **Set up CI/CD** - GitHub Actions for automatic deployment

---

## Free Hosting Options (Great for Testing)

1. **Render.com** - Free tier, auto-deploys from GitHub
2. **Railway.app** - $5 free credit/month
3. **Fly.io** - Free tier available
4. **Vercel** - Free for frontend (use with FastAPI backend)
5. **PythonAnywhere** - Free tier with limitations

---

## My Recommendation

**For getting started RIGHT NOW:**

1. Use the Flask app I created above
2. Complete the HTML templates (or use a template engine like Jinja2)
3. Deploy to **Render.com** (easiest, free tier, one-click deploy)
4. Later upgrade database to PostgreSQL when needed

**Total time to deploy:** 2-4 hours
**Cost:** Free initially, ~$7/month for production

---

## Questions to Decide:

1. **How many users?** (affects hosting choice)
2. **Public or internal?** (affects security requirements)
3. **Budget?** (free tier vs. enterprise)
4. **Timeline?** (quick MVP vs. polished product)
5. **Technical team?** (self-hosted vs. managed hosting)

Let me know your answers and I can provide a specific deployment plan!
