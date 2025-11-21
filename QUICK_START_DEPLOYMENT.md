# Quick Start: Deploy to pr.manajet.io

This is the fastest path to get Manajet running on pr.manajet.io with Sign in with Apple.

## Step 1: DNS Configuration (5 minutes)

1. **Log into your DNS provider** (Cloudflare recommended)

2. **Add CNAME record:**
   ```
   Type: CNAME
   Name: pr
   Target: [Wait for Railway URL from Step 2]
   TTL: Auto
   ```

   **Don't have the Railway URL yet?** That's OK - come back to this after Step 2.

## Step 2: Deploy to Railway (10 minutes)

```bash
# Navigate to your project
cd C:\Users\MichaelSilver\manajet-app

# Login to Railway (opens browser)
railway login

# Initialize/link project
railway init
# Choose: Create new project → Name it "manajet"

# Set environment variables
railway variables set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
railway variables set DEBUG="False"
railway variables set SESSION_COOKIE_SECURE="True"

# Deploy!
railway up

# Get your Railway URL
railway domain
```

**Copy the Railway URL** (something like `manajet-production.up.railway.app`)

**Now go back to Step 1** and add this as the CNAME target if you haven't already.

## Step 3: Add Custom Domain (2 minutes)

```bash
# Add your custom domain
railway domain pr.manajet.io
```

Railway will:
- Generate SSL certificate (takes 5-10 minutes)
- Verify your DNS is correct
- Give you a green checkmark when ready

**Wait 10-15 minutes** for:
- DNS to propagate worldwide
- SSL certificate to be issued
- Everything to be ready

Test it: https://pr.manajet.io (should load your app!)

## Step 4: Configure Apple Sign In (15 minutes)

### A. Get Your Apple Credentials

You'll need these 3 things from Apple Developer Portal:

1. **Team ID** - Go to https://developer.apple.com/account/#!/membership/
2. **Key ID** - From the private key you'll create
3. **Private Key (.p8 file)** - You'll download this

### B. Create Private Key

1. Go to https://developer.apple.com/account/resources/authkeys/list
2. Click "+" to create new key
3. Name: "Manajet Sign in with Apple"
4. Check "Sign in with Apple"
5. Click "Configure" → Select your App ID
6. Click "Continue" → "Register"
7. **Download the `.p8` file** (you can only do this ONCE!)
8. Note the **Key ID** (10 characters, like `ABC123XYZ9`)

### C. Configure Service ID

1. Go to https://developer.apple.com/account/resources/identifiers/list/serviceId
2. Click your Service ID: `io.manajet.connect10`
3. Check "Sign in with Apple"
4. Click "Configure"
5. Add domains:
   - `pr.manajet.io`
   - `localhost:5000` (for local testing)
6. Add return URLs:
   - `https://pr.manajet.io/auth/apple/callback`
   - `http://localhost:5000/auth/apple/callback`
7. Click "Save" → "Continue" → "Save"

### D. Generate Client Secret

Create a file `generate_apple_secret.py` in your project:

```python
import jwt
import time

# UPDATE THESE VALUES:
TEAM_ID = "YOUR_TEAM_ID"  # From step A
CLIENT_ID = "io.manajet.connect10"
KEY_ID = "YOUR_KEY_ID"  # From step B
KEY_FILE = "AuthKey_ABC123XYZ9.p8"  # Your downloaded file

# Read the private key
with open(KEY_FILE, 'r') as f:
    private_key = f.read()

# Generate JWT
headers = {"kid": KEY_ID, "alg": "ES256"}
payload = {
    "iss": TEAM_ID,
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400 * 180,  # 180 days
    "aud": "https://appleid.apple.com",
    "sub": CLIENT_ID
}

client_secret = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
print(f"Client Secret:\n{client_secret}")
```

Run it:
```bash
pip install pyjwt cryptography
python generate_apple_secret.py
```

**Copy the output** - this is your APPLE_CLIENT_SECRET!

### E. Set Production Environment Variables

```bash
railway variables set APPLE_CLIENT_ID="io.manajet.connect10"
railway variables set APPLE_CLIENT_SECRET="paste-your-jwt-token-here"

# Redeploy with new variables
railway up
```

## Step 5: Test Everything (5 minutes)

1. **Visit https://pr.manajet.io**
   - Should load with HTTPS (lock icon)
   - No certificate warnings

2. **Test Regular Login:**
   - Username: `admin`
   - Password: `admin123`
   - Should log you in

3. **Test Sign in with Apple:**
   - Click "Sign in with Apple" button
   - Should redirect to Apple
   - Sign in with your Apple ID
   - Should redirect back and log you in

## Troubleshooting

### DNS not working?
```bash
# Check if DNS is resolving
nslookup pr.manajet.io

# Should show your Railway URL or IP
```
**Solution**: Wait 15-30 more minutes for DNS propagation

### SSL certificate error?
**Solution**: Wait 5-10 minutes for Railway to provision certificate

### Apple OAuth error?
**Common issues:**
- `redirect_uri_mismatch`: Check URLs in Apple Developer Portal match exactly
- `invalid_client`: Client Secret might be wrong or expired
- `invalid_request`: Domain not configured in Apple Developer Portal

**Solution**: Double-check all Apple configuration steps

### App not loading?
```bash
# Check Railway logs
railway logs
```
Look for errors and fix them

## Success Checklist

- [ ] pr.manajet.io loads with HTTPS
- [ ] Regular login works
- [ ] Sign in with Apple works
- [ ] No errors in Railway logs: `railway logs`
- [ ] SSL certificate valid (lock icon)

## What's Next?

Your app is now live! Here's what you should do:

1. **Change default passwords** for admin, customer, crew accounts
2. **Set up monitoring** - Railway provides basic metrics
3. **Configure backups** - Download jet_schedule_data.json regularly
4. **Share the URL** - pr.manajet.io is ready for users!

## Quick Commands Reference

```bash
# View logs
railway logs --follow

# Check status
railway status

# Update code
git add .
git commit -m "Update"
git push
railway up

# Open in browser
railway open
```

## Need Help?

- **DNS Issues**: Check `DNS_SETUP.md`
- **Apple OAuth**: Check `APPLE_SIGNIN_SETUP.md`
- **Full Checklist**: Check `PRODUCTION_CHECKLIST.md`
- **Railway Help**: https://railway.app/help

## Time Estimate

- DNS setup: 5 min
- Railway deployment: 10 min
- Waiting for DNS/SSL: 15-20 min
- Apple configuration: 15 min
- Testing: 5 min

**Total: ~45-60 minutes**

Most of the time is waiting for DNS propagation and SSL provisioning. You can do the Apple configuration while waiting!
