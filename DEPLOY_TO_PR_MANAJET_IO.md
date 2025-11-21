# Deploy to pr.manajet.io - Complete Guide

Quick deployment guide for getting Manajet live on **pr.manajet.io** using DigitalOcean + Namecheap DNS.

## What You'll Deploy

- **Production URL**: https://pr.manajet.io
- **Hosting**: DigitalOcean App Platform
- **DNS**: Namecheap (manajet.io domain)
- **Features**: Full Manajet app + Sign in with Apple

## Time Required: ~60 minutes

- Your work: 30-35 minutes
- Waiting (DNS/SSL): 25-30 minutes

---

## Part 1: Deploy to DigitalOcean (~15 min)

### Step 1: Push Code to GitHub

```bash
cd C:\Users\MichaelSilver\manajet-app

# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Ready for pr.manajet.io deployment"

# Push
git push origin master
```

### Step 2: Create App on DigitalOcean

1. **Go to**: https://cloud.digitalocean.com/apps
2. **Click**: "Create App" (blue button)
3. **Choose GitHub**:
   - Click "GitHub"
   - Authorize DigitalOcean if needed
   - Select your repository: `manajet-app`
   - Branch: `master`
   - Autodeploy: ✅ (checked)
   - Click "Next"

### Step 3: Configure App Resources

DigitalOcean should auto-detect your app. Verify:

- **Name**: `manajet` (or whatever you prefer)
- **Region**: Choose closest (e.g., New York, San Francisco, Toronto)
- **Type**: Web Service
- **Build Command**: Should auto-detect or use: `pip install -r requirements.txt`
- **Run Command**: `gunicorn web_app:app`
- **HTTP Port**: `8080`

Click "Next"

### Step 4: Set Environment Variables

Click "Edit" next to Environment Variables and add:

```
SECRET_KEY = [Generate: python -c 'import secrets; print(secrets.token_hex(32))']
DEBUG = False
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = 3600
APPLE_CLIENT_ID = io.manajet.connect10
APPLE_CLIENT_SECRET = [Leave empty for now - will add later]
```

Mark `SECRET_KEY` and `APPLE_CLIENT_SECRET` as **encrypted** (lock icon).

Click "Save"

### Step 5: Choose Plan

- **Starter**: $5/month (512 MB RAM) - Good for testing
- **Basic**: $12/month (1 GB RAM) - **Recommended for production**
- **Professional**: $24+/month - For high traffic

Select your plan and click "Next"

### Step 6: Review and Launch

- Review all settings
- Click "Create Resources"
- **Wait 3-5 minutes** for build and deployment

You'll get a URL like: `manajet-xxxxx.ondigitalocean.app`

**✅ Checkpoint**: Visit the DigitalOcean URL - your app should load!

---

## Part 2: Configure DNS with Namecheap (~5 min)

### Step 1: Get DigitalOcean DNS Info

1. In DigitalOcean dashboard, go to your **manajet** app
2. Click **"Settings"** tab
3. Scroll to **"Domains"** section
4. Click **"Add Domain"**
5. Enter: `pr.manajet.io`
6. Click "Add Domain"

**DigitalOcean will show you**:
- Either a **CNAME** record to add
- Or an **A** record with IP address

**Copy these values** - you need them for Namecheap!

### Step 2: Add DNS Record in Namecheap

1. **Go to**: https://www.namecheap.com/ and sign in
2. Click **"Domain List"** (left sidebar)
3. Find **manajet.io** and click **"Manage"**
4. Click the **"Advanced DNS"** tab
5. Click **"Add New Record"** button

**If DigitalOcean gave you CNAME** (most common):
```
Type: CNAME Record
Host: pr
Value: [paste from DigitalOcean, e.g., lb.ondigitalocean.app]
TTL: Automatic
```

**If DigitalOcean gave you A record**:
```
Type: A Record
Host: pr
Value: [IP address from DigitalOcean]
TTL: Automatic
```

6. Click the **green checkmark (✓)** to save

### Step 3: Wait for DNS Propagation

**Typical time**: 5-30 minutes

**Check if ready**:
```bash
nslookup pr.manajet.io
```

Should return DigitalOcean's IP or domain.

Or use: https://www.whatsmydns.net/#CNAME/pr.manajet.io

---

## Part 3: SSL Certificate (Automatic, ~10 min wait)

DigitalOcean automatically provisions SSL certificates.

**Check status**:
1. Go to your app in DigitalOcean
2. Settings → Domains
3. Look for pr.manajet.io - should say "Active" with green checkmark

**When ready**:
- HTTPS will work: https://pr.manajet.io
- You'll see lock icon in browser
- No certificate warnings

**Note**: SSL provisioning starts after DNS is verified (5-10 min after DNS works)

---

## Part 4: Configure Apple Sign In (~20 min)

### Step 1: Configure Apple Developer Portal

1. **Go to**: https://developer.apple.com/account/resources/identifiers/list/serviceId
2. **Click**: Service ID `io.manajet.connect10`
3. **Enable**: Check "Sign in with Apple"
4. **Click**: "Configure" button

**Add Domains**:
```
pr.manajet.io
localhost:5000
```

**Add Return URLs**:
```
https://pr.manajet.io/auth/apple/callback
http://localhost:5000/auth/apple/callback
```

5. Click "Save" → "Continue" → "Save"

### Step 2: Create Private Key (if you haven't already)

1. **Go to**: https://developer.apple.com/account/resources/authkeys/list
2. Click **"+"** to create new key
3. **Name**: "Manajet Sign in with Apple"
4. **Check**: "Sign in with Apple"
5. Click "Configure" → Select your App ID
6. Click "Continue" → "Register"
7. **Download** the `.p8` file (you can only do this ONCE!)
8. **Note** the Key ID (e.g., `ABC123XYZ9`)

### Step 3: Get Your Team ID

1. **Go to**: https://developer.apple.com/account/#!/membership/
2. **Copy** your Team ID (10-character code)

### Step 4: Generate Client Secret

Create file: `generate_apple_secret.py`

```python
import jwt
import time

# UPDATE THESE VALUES:
TEAM_ID = "YOUR_TEAM_ID"  # From Apple Developer Membership
CLIENT_ID = "io.manajet.connect10"
KEY_ID = "YOUR_KEY_ID"  # From the private key you created
KEY_FILE = "AuthKey_XXXXX.p8"  # Path to your downloaded .p8 file

# Read the private key
with open(KEY_FILE, 'r') as f:
    private_key = f.read()

# Generate the JWT
headers = {"kid": KEY_ID, "alg": "ES256"}
payload = {
    "iss": TEAM_ID,
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400 * 180,  # 180 days (Apple's max)
    "aud": "https://appleid.apple.com",
    "sub": CLIENT_ID
}

client_secret = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
print(f"Client Secret (valid for 180 days):\n{client_secret}")
```

**Run it**:
```bash
pip install pyjwt cryptography
python generate_apple_secret.py
```

**Copy the output** - this is your APPLE_CLIENT_SECRET!

### Step 5: Update Environment Variables in DigitalOcean

1. Go to your app in DigitalOcean dashboard
2. Click **"Settings"**
3. Scroll to **"App-Level Environment Variables"**
4. Click **"Edit"**
5. Find `APPLE_CLIENT_SECRET`
6. Paste your JWT token
7. Mark it as **encrypted** (lock icon)
8. Click **"Save"**

**DigitalOcean will automatically redeploy** your app (takes 2-3 minutes).

---

## Part 5: Test Everything (~5 min)

### Test 1: HTTPS Works

Visit: **https://pr.manajet.io**

Should see:
- ✅ Lock icon (valid SSL)
- ✅ Manajet login page
- ✅ No certificate warnings

### Test 2: Regular Login

- Username: `admin`
- Password: `admin123`

Should log you in successfully.

### Test 3: Sign in with Apple

1. Log out
2. Click **"Sign in with Apple"** button
3. Should redirect to Apple's login page
4. Sign in with your Apple ID
5. Should redirect back to pr.manajet.io
6. Should be logged in

**If any test fails**, see Troubleshooting section below.

---

## Troubleshooting

### DNS not resolving

**Problem**: `nslookup pr.manajet.io` returns nothing

**Solutions**:
1. Wait 15-30 more minutes
2. Check DNS record is saved in Namecheap (green checkmark)
3. Verify Host is `pr` (not `pr.manajet.io`)
4. Flush your DNS cache:
   ```bash
   ipconfig /flushdns
   ```

### SSL Certificate Pending

**Problem**: pr.manajet.io loads but shows certificate error

**Solutions**:
1. Wait 10-15 minutes after DNS is working
2. Check domain status in DigitalOcean (Settings → Domains)
3. Verify DNS is pointing to correct DigitalOcean domain/IP

### Apple OAuth Error

**Problem**: "redirect_uri_mismatch" or similar error

**Solutions**:
1. Verify callback URL in Apple Developer Portal is exactly:
   `https://pr.manajet.io/auth/apple/callback`
2. No trailing slash
3. Must be HTTPS (not HTTP)
4. Wait 5-10 minutes after updating Apple settings

**Problem**: "invalid_client" error

**Solutions**:
1. Check APPLE_CLIENT_SECRET is set correctly in DigitalOcean
2. Verify Client Secret isn't expired (180 days max)
3. Regenerate Client Secret if needed

### App Not Loading

**Check DigitalOcean logs**:
1. Go to app dashboard
2. Click "Runtime Logs" tab
3. Look for error messages

**Common issues**:
- Missing dependencies
- Wrong run command
- Environment variables not set

---

## Post-Deployment Checklist

- [ ] pr.manajet.io loads with HTTPS
- [ ] Login page displays correctly
- [ ] Regular login works (admin/admin123)
- [ ] Sign in with Apple works
- [ ] No errors in DigitalOcean logs
- [ ] DNS is resolving correctly
- [ ] SSL certificate is valid
- [ ] All environment variables set
- [ ] Mobile responsive (test on phone)

---

## Maintenance

### Update Your App

Push changes to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin master
```

DigitalOcean auto-deploys (if autodeploy is enabled).

### View Logs

DigitalOcean dashboard → Your app → "Runtime Logs"

### Monitor Usage

DigitalOcean dashboard → Your app → "Insights"

### Renew Apple Client Secret

**Every 180 days**:
1. Regenerate JWT using generate_apple_secret.py
2. Update APPLE_CLIENT_SECRET in DigitalOcean
3. Mark calendar for next renewal

---

## Quick Commands Reference

```bash
# Check DNS
nslookup pr.manajet.io

# Flush DNS cache (Windows)
ipconfig /flushdns

# Test HTTPS
curl -I https://pr.manajet.io

# Push updates
git add .
git commit -m "Update"
git push origin master

# Generate secret key
python -c 'import secrets; print(secrets.token_hex(32))'

# Check Python version
python --version
```

---

## Cost Summary

**DigitalOcean App Platform**:
- Starter: $5/month
- Basic: $12/month (recommended)
- Professional: $24/month

**Namecheap Domain** (if needed):
- .io domain: ~$32.98/year

**Total Monthly**: $12-$24 (plus annual domain cost)

---

## Success!

When everything is working:

✅ **Production URL**: https://pr.manajet.io
✅ **HTTPS**: Valid SSL certificate
✅ **Login**: Working (traditional + Apple)
✅ **Features**: All functionality operational
✅ **Monitoring**: Logs accessible in DigitalOcean

**Next steps**:
- Change default admin password
- Add real users
- Monitor usage and performance
- Set up automated backups
- Configure uptime monitoring

---

## Support

- **DigitalOcean**: https://docs.digitalocean.com/products/app-platform/
- **Namecheap DNS**: https://www.namecheap.com/support/knowledgebase/category/39/dns/
- **Apple Sign In**: https://developer.apple.com/sign-in-with-apple/

---

**Deployment Date**: _______________
**Deployed By**: __________________
**Production URL**: https://pr.manajet.io
**Status**: ⬜ In Progress  ⬜ Complete
