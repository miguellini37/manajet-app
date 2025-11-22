# Deploy Manajet to DigitalOcean RIGHT NOW

## Quick Deployment (10 minutes)

Your code is already pushed to GitHub! Let's deploy it now.

### Step 1: Open DigitalOcean (2 minutes)

1. Go to https://cloud.digitalocean.com/apps
2. Sign in to your DigitalOcean account
3. Click **"Create App"** button

### Step 2: Connect GitHub (2 minutes)

1. **Source:** Select **GitHub**
2. Click **"Manage Access"** if needed
3. **Authorize DigitalOcean** to access your repos
4. **Select Repository:** `miguellini37/manajet-app`
5. **Branch:** `master`
6. **Autodeploy:** ✅ Check "Autodeploy code changes"
7. Click **"Next"**

### Step 3: Configure Resources (1 minute)

DigitalOcean should auto-detect:
- **Type:** Web Service
- **Dockerfile:** Detected ✅
- **HTTP Port:** 5000
- **Build Command:** Auto-detected
- **Run Command:** Auto-detected

If not auto-detected, use these settings:
- **Dockerfile Path:** `Dockerfile`
- **HTTP Port:** `5000`
- **Run Command:** `gunicorn --bind 0.0.0.0:5000 web_app:app`

Click **"Next"**

### Step 4: Set Environment Variables (2 minutes)

**CRITICAL:** Add these environment variables:

1. Click **"Edit"** next to your web service
2. Scroll to **Environment Variables**
3. Click **"Add Variable"**
4. Add each of these:

```
SECRET_KEY = (Generate with command below)
DEBUG = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = Lax
PERMANENT_SESSION_LIFETIME = 3600
PORT = 5000
```

**Generate SECRET_KEY:**

Open a terminal and run:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output (looks like: `a4f3b2c1...`) and paste as SECRET_KEY value

**Mark SECRET_KEY as encrypted:**
- Check the 🔒 icon next to SECRET_KEY

Click **"Save"** and then **"Next"**

### Step 5: Choose Plan (1 minute)

**Recommended for starting:**
- **Plan:** Basic
- **Size:** $5/month (512 MB RAM, 1 vCPU)
- **Containers:** 1

For production with more users, upgrade to:
- **$12/month** (1 GB RAM) - Recommended
- **$24/month** (2 GB RAM) - For heavy usage

Click **"Next"**

### Step 6: Name & Deploy (2 minutes)

1. **App Name:** `manajet` (or whatever you prefer)
2. **Region:** Choose closest to your users
   - US East (New York) - Default
   - US West (San Francisco)
   - Europe (Frankfurt, Amsterdam, London)
   - Asia (Singapore, Bangalore)

3. Review everything
4. Click **"Create Resources"**

**Deployment starts!** Takes 5-10 minutes.

### Step 7: Get Your URL

1. Wait for deployment to complete (progress bar)
2. When done, you'll see: **"App is live!"**
3. Your URL will be shown:
   ```
   https://manajet-xxxxx.ondigitalocean.app
   ```
4. **COPY THIS URL** - You need it for iOS app!

### Step 8: Test Your Backend

1. Open your app URL in browser
2. You should see the Manajet login page
3. Try logging in:
   - Username: `admin`
   - Password: `admin123`

If login works, **DEPLOYMENT SUCCESSFUL!** ✅

## Troubleshooting

### Build Failed?

**Check build logs:**
1. Click on your app
2. Go to **"Runtime Logs"**
3. Look for error messages

**Common issues:**
- Missing environment variables → Go back and add SECRET_KEY
- Python version mismatch → Should use Python 3.11 from Dockerfile
- Missing dependencies → Check requirements.txt

### App Won't Start?

1. Check **"Runtime Logs"**
2. Look for errors like:
   - `SECRET_KEY not set` → Add environment variable
   - `Port already in use` → Should auto-resolve
   - `Import error` → Check all files pushed to GitHub

### Can't Access App?

1. Verify deployment completed (not still building)
2. Check if URL is correct
3. Try incognito/private browsing mode
4. Clear browser cache

### Need to Redeploy?

Just push to GitHub:
```bash
git push origin master
```

With autodeploy enabled, DigitalOcean rebuilds automatically!

## What's Next?

Once your app is deployed:

1. ✅ **Test all features** on production URL
2. ✅ **Initialize data:**
   ```bash
   # In DigitalOcean Console (Apps → Runtime Logs → Console)
   python setup_initial_data.py
   ```
3. ✅ **Update iOS app** to use production URL (see below)
4. ✅ **Set up custom domain** (optional)

## Update iOS App (Next Section)

Your production URL: `https://manajet-xxxxx.ondigitalocean.app`

See `UPDATE_IOS_FOR_PRODUCTION.md` for instructions to point iOS app to production.

## Custom Domain (Optional)

Want to use `app.yourdomain.com` instead of DigitalOcean URL?

1. In DigitalOcean: Apps → Settings → Domains
2. Click **"Add Domain"**
3. Enter your domain: `app.yourdomain.com`
4. DigitalOcean provides DNS records to add
5. Add CNAME record to your DNS provider
6. Wait for DNS propagation (5-60 minutes)

## Monitoring

**View your app stats:**
- Apps → Your App → **Insights**
- See CPU, Memory, Bandwidth usage
- Monitor response times
- Check error rates

**Set up alerts:**
- Apps → Your App → **Settings** → **Alerts**
- Get notified if app goes down
- Alert on high CPU/memory usage

## Scaling

Need more power?

1. Apps → Your App → **Settings**
2. **Edit Plan**
3. Choose larger instance size
4. Click **"Save"**
5. App redeploys with more resources

## Costs

- **Basic $5/mo:** Good for testing, light usage
- **Basic $12/mo:** Recommended for production
- **Pro $24/mo+:** High traffic, multiple users

**Included:**
- 40 GB bandwidth/month (Basic)
- 100 GB bandwidth/month (Pro)
- Automatic SSL certificates
- DDoS protection

## Support

**DigitalOcean Resources:**
- Documentation: https://docs.digitalocean.com/products/app-platform/
- Community: https://www.digitalocean.com/community/
- Support: https://cloud.digitalocean.com/support/tickets

**Your App Dashboard:**
- https://cloud.digitalocean.com/apps

---

🚀 **Your backend is now live on DigitalOcean!**

**Next:** Update iOS app to use production URL
