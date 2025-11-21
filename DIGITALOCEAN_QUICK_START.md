# DigitalOcean Quick Deploy - 5 Minutes!

## Prerequisites
- DigitalOcean account ([Sign up here - $200 free credit](https://try.digitalocean.com/freetrialoffer/))
- Your code pushed to GitHub

## Deploy in 4 Steps

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin master
```

### Step 2: Create App on DigitalOcean

Visit: **[cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)**

Click **"Create App"**

### Step 3: Configure

1. **Source**: Select GitHub → Choose your repo → Branch: `master`
2. **Resources**: DigitalOcean auto-detects Dockerfile ✅
3. **Environment Variables**: Add ONE variable:
   ```
   SECRET_KEY = [paste generated key]
   ```

   **Generate key:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Plan**: Select **Basic - $5/month**

### Step 4: Deploy!

Click **"Create Resources"**

Wait 3-5 minutes... ☕

---

## Done! 🎉

Your app is live at: `https://your-app.ondigitalocean.app`

### First Login

After deployment, initialize sample data:

1. Go to your app → **Console** tab
2. Run: `python setup_initial_data.py`
3. Login with:
   - Username: `admin`
   - Password: `admin123`

---

## What You Get

✅ Live app with HTTPS
✅ Auto-deployments on git push
✅ Free SSL certificate
✅ 99.99% uptime SLA
✅ Auto-scaling
✅ Zero-downtime deployments

**Cost: $5/month**

---

## Need Help?

Full guide: [DIGITALOCEAN_DEPLOYMENT.md](DIGITALOCEAN_DEPLOYMENT.md)
