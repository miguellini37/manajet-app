# DigitalOcean App Platform Deployment Guide

Deploy your Manajet app to DigitalOcean App Platform in 5 minutes!

## Why App Platform?

✅ **No server management** - Focus on your app, not infrastructure
✅ **Auto-scaling** - Handles traffic spikes automatically
✅ **Free SSL/HTTPS** - Built-in Let's Encrypt certificates
✅ **Auto-deployments** - Push to GitHub and it deploys automatically
✅ **$5/month** - Start small, scale as needed

---

## Quick Deploy (5 Minutes)

### Option 1: Deploy via Web UI (Easiest)

#### Step 1: Push Your Code to GitHub

```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for DigitalOcean deployment"
git push origin master
```

#### Step 2: Create App on DigitalOcean

1. **Go to App Platform**: Visit [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)

2. **Click "Create App"**

3. **Connect GitHub**:
   - Select "GitHub"
   - Authorize DigitalOcean to access your repos
   - Choose your repository: `mikemanajet/manajet-app-1`
   - Select branch: `master`
   - ✅ Check "Autodeploy" (deploys on every push)

4. **Configure the App**:
   - DigitalOcean will auto-detect the Dockerfile
   - **Name**: `manajet` (or any name you like)
   - **Region**: Choose closest to you (NYC, San Francisco, etc.)
   - **Plan**: Start with **Basic ($5/month)**

5. **Set Environment Variables**:
   Click "Edit" next to environment variables and add:

   ```
   SECRET_KEY = [Generate secure key - see below]
   DEBUG = False
   SESSION_COOKIE_SECURE = True
   PORT = 5000
   ```

   **To generate SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste as SECRET_KEY value.

6. **Review and Create**:
   - Review your settings
   - Click "Create Resources"
   - Wait 3-5 minutes for deployment

7. **Get Your URL**:
   - Once deployed, you'll see your live URL
   - Example: `https://manajet-abc123.ondigitalocean.app`

8. **Initialize Sample Data**:
   - Go to your app's Console tab
   - Run: `python setup_initial_data.py`
   - Or use the web interface to create your first admin user

---

### Option 2: Deploy via doctl CLI

#### Install doctl (DigitalOcean CLI)

**Windows:**
```powershell
# Using Chocolatey
choco install doctl

# Or download from: https://github.com/digitalocean/doctl/releases
```

**Mac:**
```bash
brew install doctl
```

**Linux:**
```bash
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.104.0/doctl-1.104.0-linux-amd64.tar.gz
tar xf doctl-*.tar.gz
sudo mv doctl /usr/local/bin
```

#### Authenticate

```bash
# Get API token from: https://cloud.digitalocean.com/account/api/tokens
doctl auth init
```

Paste your API token when prompted.

#### Deploy

```bash
# Generate secret key first
python -c "import secrets; print(secrets.token_hex(32))"

# Deploy the app
doctl apps create --spec .do/app.yaml

# Get app ID from output, then check status
doctl apps list

# Update environment variable with your SECRET_KEY
doctl apps update YOUR_APP_ID --spec .do/app.yaml
```

---

## Post-Deployment Setup

### 1. Access Your App

Visit your DigitalOcean URL (e.g., `https://manajet-abc123.ondigitalocean.app`)

### 2. Initialize Data

**Option A: Via Console**
1. Go to DigitalOcean App Platform dashboard
2. Click your app → Console tab
3. Run: `python setup_initial_data.py`

**Option B: Via Local Script** (if you have doctl)
```bash
doctl apps exec YOUR_APP_ID --component web -- python setup_initial_data.py
```

### 3. Login

Default credentials (CHANGE THESE!):
- Username: `admin`
- Password: `admin123`

### 4. Set Up Custom Domain (Optional)

1. Go to app settings → Domains
2. Add your domain: `manajet.yourdomain.com`
3. Add DNS records as shown:
   - Type: `CNAME`
   - Name: `manajet`
   - Value: `your-app.ondigitalocean.app`

SSL certificate is automatically provisioned!

---

## Configuration

### Environment Variables

Set these in the App Platform UI or in `.do/app.yaml`:

| Variable | Required | Value |
|----------|----------|-------|
| `SECRET_KEY` | ✅ Yes | Generate with `secrets.token_hex(32)` |
| `DEBUG` | No | `False` (always False in production) |
| `SESSION_COOKIE_SECURE` | No | `True` (enables HTTPS-only cookies) |
| `PORT` | No | `5000` |

### Pricing

**Basic Plan**: $5/month
- 512 MB RAM
- 1 vCPU
- Perfect for getting started

**Professional Plan**: $12/month
- 1 GB RAM
- More resources for higher traffic

You can upgrade anytime as your app grows!

---

## Auto-Deployments

Every time you push to GitHub, DigitalOcean automatically:
1. Pulls latest code
2. Builds new Docker image
3. Deploys with zero downtime
4. Runs health checks

```bash
# Make changes
git add .
git commit -m "Add new feature"
git push origin master

# Auto-deploys in 3-5 minutes!
```

---

## Monitoring

### View Logs

**Via Web UI:**
1. Go to your app → Runtime Logs
2. Filter by component (web)
3. Search for errors or specific events

**Via CLI:**
```bash
doctl apps logs YOUR_APP_ID --type run
doctl apps logs YOUR_APP_ID --type build
doctl apps logs YOUR_APP_ID --follow  # Live logs
```

### Health Checks

App Platform automatically monitors your app:
- Checks `/login` endpoint every 30 seconds
- Restarts if health check fails 3 times
- Zero-downtime deployments

### Metrics

View in dashboard:
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

---

## Data Persistence

### Using JSON File (Current Setup)

Your `jet_schedule_data.json` persists between deployments because:
- Data stored in app's filesystem
- Survives app restarts
- **Warning**: Data lost if you destroy the app

**Backup your data regularly:**
```bash
# Download via doctl
doctl apps exec YOUR_APP_ID --component web -- cat jet_schedule_data.json > backup.json
```

### Upgrade to Managed Database (Recommended for Production)

Add PostgreSQL to your app:

1. **Via Web UI**:
   - Go to app settings → Database
   - Add PostgreSQL database ($15/month)
   - Database connection string automatically added as env var

2. **Update app.yaml**:
   ```yaml
   databases:
   - name: manajet-db
     engine: PG
     version: "15"
     production: false
   ```

3. **Modify `jet_manager.py`** to use PostgreSQL instead of JSON

Benefits:
- ✅ Automated backups (daily)
- ✅ Point-in-time recovery
- ✅ High availability
- ✅ Automatic scaling

---

## Scaling Your App

### Vertical Scaling (More Resources)

```bash
# Upgrade to Professional plan
# Via Web UI: Settings → Plan → Professional ($12/month)

# Or via CLI
doctl apps update YOUR_APP_ID --spec .do/app.yaml
```

### Horizontal Scaling (More Instances)

Update `.do/app.yaml`:
```yaml
services:
- name: web
  instance_count: 3  # Run 3 instances
```

App Platform automatically load-balances between instances!

---

## Troubleshooting

### App Won't Deploy

```bash
# Check build logs
doctl apps logs YOUR_APP_ID --type build

# Common issues:
# - Missing Dockerfile: Ensure Dockerfile exists in root
# - Dependencies: Check requirements.txt
# - Build timeout: Optimize Dockerfile layers
```

### App Crashes on Startup

```bash
# Check runtime logs
doctl apps logs YOUR_APP_ID --type run

# Common issues:
# - Missing SECRET_KEY: Set in environment variables
# - Port mismatch: Ensure PORT=5000
# - Import errors: Verify all files in repo
```

### Can't Access App

- Check app status: Should show "Active"
- Verify health checks are passing
- Check firewall/security rules
- Try incognito mode (clear cache)

### Data Loss

If using JSON storage:
```bash
# Restore from backup
# 1. Access console
# 2. Upload backup.json
# 3. Overwrite jet_schedule_data.json
```

For production, **use managed database** to prevent data loss!

---

## Security Best Practices

### 1. Change Default Passwords

After first login:
- Change admin password immediately
- Delete or update all sample users

### 2. Secure Environment Variables

- Never commit `.env` to git
- Use DigitalOcean's secret management
- Rotate SECRET_KEY periodically

### 3. Enable HTTPS Only

Already configured! App Platform provides:
- Free SSL certificates (Let's Encrypt)
- Automatic renewal
- HTTPS redirect (optional)

### 4. Regular Backups

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
doctl apps exec YOUR_APP_ID --component web -- cat jet_schedule_data.json > backups/backup_$DATE.json
```

Run daily with cron or Task Scheduler.

---

## Advanced Configuration

### Custom Dockerfile

App Platform uses your `Dockerfile`. To customize:

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["gunicorn", "web_app:app"]
```

### Add Redis for Sessions

```yaml
services:
- name: redis
  engine: REDIS
  version: "7"

envs:
- key: REDIS_URL
  scope: RUN_TIME
  value: ${redis.REDIS_URL}
```

### CI/CD Pipeline

App Platform automatically handles CI/CD, but you can add GitHub Actions:

```yaml
# .github/workflows/tests.yml
name: Run Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: pytest
```

---

## Cost Optimization

1. **Start Small**: Basic plan ($5/month) is perfect for development
2. **Monitor Usage**: Check metrics to see if you need more resources
3. **Scale Smartly**: Only upgrade when you hit limits
4. **Use Spot Instances**: For dev/staging environments
5. **Database**: Start without managed DB, add later if needed

**Estimated Monthly Cost:**
- Basic App: $5
- With PostgreSQL: $20 ($5 + $15)
- Professional + DB: $27 ($12 + $15)

---

## Migration from Other Platforms

### From Railway

Your app is already compatible! Just:
1. Push to GitHub
2. Create app on DigitalOcean
3. Copy environment variables
4. Deploy

### From Heroku

1. Export data from Heroku
2. Push code to GitHub
3. Deploy to App Platform
4. Import data via console

---

## Next Steps

After deploying:

1. ✅ Set up custom domain
2. ✅ Configure automated backups
3. ✅ Set up monitoring/alerts
4. ✅ Add managed PostgreSQL database
5. ✅ Configure email service (for notifications)
6. ✅ Set up staging environment

---

## Support & Resources

- **App Platform Docs**: https://docs.digitalocean.com/products/app-platform/
- **Community**: https://www.digitalocean.com/community/
- **Support Tickets**: Available in dashboard
- **Status Page**: https://status.digitalocean.com/

---

## Summary

**To Deploy:**
1. Push code to GitHub
2. Go to cloud.digitalocean.com/apps
3. Create app → Connect GitHub → Select repo
4. Add SECRET_KEY environment variable
5. Deploy!

**Your URL:** `https://your-app.ondigitalocean.app`
**Cost:** Starting at $5/month
**Deploy Time:** 3-5 minutes

**Your Manajet app is production-ready on DigitalOcean! 🚀**
