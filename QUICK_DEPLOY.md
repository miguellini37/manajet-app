# Quick Deploy to Railway - 5 Minutes!

## Option 1: Use the Deployment Script (Easiest)

### On Windows:
```cmd
deploy-to-railway.bat
```

### On Mac/Linux:
```bash
./deploy-to-railway.sh
```

That's it! The script will:
1. Log you into Railway
2. Initialize your project
3. Generate a secure secret key
4. Set all environment variables
5. Deploy your application

---

## Option 2: Manual Deployment (Step by Step)

Open your terminal and run these commands:

### 1. Login to Railway
```bash
railway login
```
This will open your browser. Sign in with GitHub, Google, or Email.

### 2. Initialize Project
```bash
railway init
```
- Choose "Create new project"
- Name it "manajet" (or any name you like)

### 3. Set Environment Variables

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and set it:
```bash
railway variables set SECRET_KEY="paste-your-secret-key-here"
railway variables set DEBUG="False"
railway variables set SESSION_COOKIE_SECURE="True"
```

### 4. Deploy!
```bash
railway up
```

Wait 2-3 minutes for the build to complete.

### 5. Get Your URL
```bash
railway domain
```

Click the URL or copy it to your browser!

---

## After Deployment

### View Your Application
```bash
railway open
```

### Check Logs
```bash
railway logs
```

### Monitor Deployment
```bash
railway status
```

---

## Login Credentials

Use these default credentials (CHANGE THEM AFTER FIRST LOGIN):

**Admin:**
- Username: `admin`
- Password: `admin123`

**Customer:**
- Username: `johnsmith`
- Password: `customer123`

---

## Troubleshooting

### If deployment fails:

1. **Check logs:**
   ```bash
   railway logs
   ```

2. **Verify environment variables:**
   ```bash
   railway variables
   ```

3. **Redeploy:**
   ```bash
   railway up
   ```

### If app won't start:

Make sure these files exist:
- ✅ Procfile
- ✅ requirements.txt
- ✅ web_app.py

### Need help?

Visit Railway docs: https://docs.railway.app/

---

## You're Done! 🎉

Your beautiful Manajet app should now be live at your Railway URL!
