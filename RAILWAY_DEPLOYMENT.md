# Railway Deployment Guide for Manajet

This guide will walk you through deploying your Manajet application to Railway.

## Prerequisites

- A [Railway](https://railway.app/) account (sign up for free)
- Git installed on your local machine
- Your code committed to a Git repository (GitHub, GitLab, or Bitbucket)

## Quick Deploy (Recommended)

### Step 1: Commit Your Changes

Make sure all your recent changes are committed to your Git repository:

```bash
git add .
git commit -m "Prepare for Railway deployment with modern UI"
git push origin master
```

### Step 2: Deploy to Railway

1. **Go to Railway**: Visit [railway.app](https://railway.app/) and sign in

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select your `manajet-app` repository

3. **Configure Environment Variables**:
   Railway will automatically detect your Flask app. Now add these environment variables:

   - Click on your project → Variables tab
   - Add the following variables:

   ```
   SECRET_KEY=generate-a-random-secret-key-here-use-at-least-32-characters
   DEBUG=False
   SESSION_COOKIE_SECURE=True
   PERMANENT_SESSION_LIFETIME=3600
   ```

   **Important**: Generate a secure SECRET_KEY! You can use this Python command:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Deploy**:
   - Railway will automatically build and deploy your application
   - Wait for the deployment to complete (usually 2-3 minutes)

5. **Get Your URL**:
   - Go to Settings → Domains
   - Click "Generate Domain"
   - Railway will give you a URL like: `https://your-app-name.up.railway.app`

6. **Visit Your App**:
   - Click on the generated URL
   - You should see your beautiful Manajet application!

## Alternative: Railway CLI Deployment

### Step 1: Install Railway CLI

```bash
# On macOS/Linux
curl -fsSL https://railway.app/install.sh | sh

# On Windows (using npm)
npm i -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Initialize Project

```bash
# In your project directory
railway init
```

### Step 4: Set Environment Variables

```bash
railway variables set SECRET_KEY="your-super-secret-key-here"
railway variables set DEBUG="False"
railway variables set SESSION_COOKIE_SECURE="True"
```

### Step 5: Deploy

```bash
railway up
```

### Step 6: Get Your URL

```bash
railway domain
```

## Post-Deployment Setup

### 1. Initialize Sample Data

After first deployment, you may need to initialize your data:

1. SSH into your Railway instance or use the Railway CLI:
   ```bash
   railway run python setup_initial_data.py
   ```

2. Or manually create users through the application interface

### 2. Test Your Application

Login with the default credentials (remember to change these!):

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Customer Account:**
- Username: `johnsmith`
- Password: `customer123`

### 3. Verify Functionality

Test the following:
- ✅ Login/logout works
- ✅ Dashboard loads with stats
- ✅ Navigation works
- ✅ Can create new flights
- ✅ Can manage passengers
- ✅ Mobile responsive design works

## Important Security Steps

⚠️ **Before going live, you MUST:**

1. **Change Default Passwords**:
   - Login as admin
   - Change all default user passwords
   - Or delete sample users and create new ones

2. **Generate Secure SECRET_KEY**:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Update this in Railway environment variables

3. **Enable HTTPS** (Railway does this automatically)

4. **Review Data Persistence**:
   - By default, data is stored in `jet_schedule_data.json`
   - For production, consider using Railway's PostgreSQL database
   - Or use Railway's persistent volume storage

## Monitoring Your Application

### View Logs

```bash
railway logs
```

Or visit the Railway dashboard → Deployments → View logs

### Monitor Performance

Railway provides built-in metrics:
- CPU usage
- Memory usage
- Request count
- Response times

Access these in: Project → Metrics

## Updating Your Application

When you make changes:

1. Commit and push to your repository:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin master
   ```

2. Railway will automatically detect changes and redeploy

Or using Railway CLI:
```bash
railway up
```

## Custom Domain (Optional)

To use your own domain:

1. Go to Railway dashboard → Settings → Domains
2. Click "Custom Domain"
3. Enter your domain (e.g., `manajet.yourdomain.com`)
4. Add the CNAME record to your DNS provider:
   - Type: `CNAME`
   - Name: `manajet` (or your subdomain)
   - Value: Your Railway domain

## Troubleshooting

### Application Won't Start

Check logs for errors:
```bash
railway logs
```

Common issues:
- Missing environment variables
- Python dependencies not installed
- Port configuration issues

### 502 Bad Gateway

- Check that gunicorn is starting correctly
- Verify PORT environment variable is set
- Check application logs for startup errors

### Static Files Not Loading

Railway automatically serves static files. If issues persist:
- Verify `static/` directory exists
- Check file paths in templates
- Clear browser cache

### Database/Data Issues

If using JSON storage:
- Data persists between deployments
- Consider using Railway volumes for guaranteed persistence
- For production, migrate to PostgreSQL

## Scaling (Railway Pro)

Railway offers autoscaling:
- Go to Settings → Scale
- Configure replicas and resources
- Set up autoscaling rules

## Cost Estimation

Railway pricing:
- **Hobby Plan**: $5/month (includes $5 usage credit)
- **Pro Plan**: $20/month (includes $20 usage credit)
- Free trial available

Your Manajet app should run comfortably on the Hobby plan.

## Support

- **Railway Docs**: https://docs.railway.app/
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app/

## Next Steps

After successful deployment:

1. ✅ Set up monitoring and alerts
2. ✅ Configure automatic backups for your data
3. ✅ Set up a staging environment for testing
4. ✅ Consider migrating to PostgreSQL for better performance
5. ✅ Implement rate limiting for API endpoints
6. ✅ Set up error tracking (e.g., Sentry)

---

**Your Manajet application is now deployed! 🚀**

Access it at your Railway domain and enjoy your beautiful, modern private jet management system.
