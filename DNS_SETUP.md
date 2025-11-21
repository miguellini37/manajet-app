# DNS Setup Guide for pr.manajet.io

This guide will help you configure DNS for your Manajet production deployment.

## Domain Information

- **Production Domain**: `pr.manajet.io`
- **Root Domain**: `manajet.io`
- **Subdomain**: `pr`

## Deployment Platform

Based on your project setup, you're using **Railway** for deployment.

## DNS Configuration Steps

### 1. Get Railway Domain Information

First, deploy your app to Railway and get the deployment URL:

```bash
# Login to Railway
railway login

# Link to your project (if not already)
railway link

# Deploy
railway up

# Get your Railway domain
railway domain
```

Railway will provide you with:
- **Railway URL**: Something like `manajet-app-production.up.railway.app`
- Or a custom domain setup option

### 2. Configure DNS Records

You need to add DNS records for `pr.manajet.io` in your domain registrar or DNS provider (e.g., Cloudflare, GoDaddy, Namecheap, Route 53).

#### Option A: Using CNAME (Recommended)

If Railway provides a permanent URL:

| Type  | Name | Value                                    | TTL  |
|-------|------|------------------------------------------|------|
| CNAME | pr   | your-app-name.up.railway.app            | Auto |

#### Option B: Using A Record

If Railway provides an IP address:

| Type | Name | Value        | TTL  |
|------|------|--------------|------|
| A    | pr   | xxx.xxx.x.xx | Auto |

### 3. Common DNS Providers

#### Cloudflare (Recommended for SSL)

1. Log into Cloudflare dashboard
2. Select your domain `manajet.io`
3. Go to "DNS" section
4. Click "Add record"
5. Configure:
   - **Type**: CNAME
   - **Name**: pr
   - **Target**: your-railway-app.up.railway.app
   - **Proxy status**: Proxied (🟠) - enables Cloudflare SSL
   - **TTL**: Auto
6. Click "Save"

**Cloudflare Benefits**:
- Free SSL certificate
- DDoS protection
- CDN caching
- Analytics

#### GoDaddy

1. Log into GoDaddy
2. Go to "My Products" → "Domains"
3. Click "DNS" next to manajet.io
4. Click "Add" under Records
5. Configure:
   - **Type**: CNAME
   - **Name**: pr
   - **Value**: your-railway-app.up.railway.app
   - **TTL**: 1 Hour
6. Click "Save"

#### Namecheap

1. Log into Namecheap
2. Click "Domain List"
3. Click "Manage" next to manajet.io
4. Go to "Advanced DNS"
5. Click "Add New Record"
6. Configure:
   - **Type**: CNAME Record
   - **Host**: pr
   - **Value**: your-railway-app.up.railway.app
   - **TTL**: Automatic
7. Click the green checkmark to save

#### AWS Route 53

1. Log into AWS Console
2. Go to Route 53
3. Select hosted zone for `manajet.io`
4. Click "Create record"
5. Configure:
   - **Record name**: pr
   - **Record type**: CNAME
   - **Value**: your-railway-app.up.railway.app
   - **TTL**: 300
6. Click "Create records"

### 4. Configure Custom Domain in Railway

After DNS is configured:

```bash
# Add custom domain to Railway
railway domain pr.manajet.io
```

Or via Railway dashboard:
1. Go to your project
2. Click "Settings"
3. Scroll to "Domains"
4. Click "Custom Domain"
5. Enter: `pr.manajet.io`
6. Click "Add"

Railway will:
- Generate an SSL certificate automatically
- Provide you with DNS records to configure (if not already done)
- Verify domain ownership

### 5. Verify DNS Propagation

Use these tools to check if DNS is working:

```bash
# Command line
nslookup pr.manajet.io
dig pr.manajet.io

# Or use online tools:
```

**Online Tools**:
- https://www.whatsmydns.net/#CNAME/pr.manajet.io
- https://dnschecker.org/
- https://mxtoolbox.com/SuperTool.aspx

**Note**: DNS propagation can take 5 minutes to 48 hours depending on:
- TTL settings
- DNS provider
- Your location
- ISP DNS cache

Typically takes 15-30 minutes.

### 6. Update Apple Sign In Configuration

Once DNS is working, update your Apple Developer Portal:

1. Go to [Apple Developer Portal](https://developer.apple.com/account/)
2. Navigate to "Certificates, Identifiers & Profiles"
3. Click "Identifiers"
4. Select your Service ID: `io.manajet.connect10`
5. Click "Configure" next to "Sign in with Apple"
6. Under "Return URLs", add:
   ```
   https://pr.manajet.io/auth/apple/callback
   ```
7. Under "Domains and Subdomains", add:
   ```
   pr.manajet.io
   ```
8. Click "Save" → "Continue" → "Save"

### 7. Update Environment Variables

Set the correct callback URL for production:

```bash
# For Railway
railway variables set CALLBACK_URL="https://pr.manajet.io"
```

## SSL/HTTPS Configuration

### Railway (Automatic)
Railway automatically provisions SSL certificates via Let's Encrypt when you add a custom domain. No additional configuration needed.

### Cloudflare (If using)
1. Ensure SSL/TLS encryption mode is set to "Full" or "Full (strict)"
2. Go to SSL/TLS → Edge Certificates
3. Enable "Always Use HTTPS"
4. Enable "Automatic HTTPS Rewrites"

## Testing the Setup

### 1. Check DNS Resolution

```bash
# Should return Railway's IP or CNAME target
nslookup pr.manajet.io
```

### 2. Check HTTPS

Visit: https://pr.manajet.io

Should show:
- Valid SSL certificate (lock icon)
- Your Manajet application
- No certificate warnings

### 3. Test Sign in with Apple

1. Go to https://pr.manajet.io/login
2. Click "Sign in with Apple"
3. Should redirect to Apple's login
4. After authentication, should redirect back to https://pr.manajet.io

## Troubleshooting

### DNS Not Resolving

**Problem**: `nslookup pr.manajet.io` returns no results

**Solutions**:
1. Check DNS record is saved in your provider
2. Wait for propagation (15-30 minutes)
3. Try flushing your local DNS cache:
   ```bash
   # Windows
   ipconfig /flushdns

   # Mac
   sudo dscacheutil -flushcache

   # Linux
   sudo systemd-resolve --flush-caches
   ```
4. Try a different DNS server (8.8.8.8 - Google DNS)

### SSL Certificate Errors

**Problem**: "Your connection is not private" or "NET::ERR_CERT_COMMON_NAME_INVALID"

**Solutions**:
1. Wait for Railway to provision certificate (can take 5-10 minutes)
2. Verify custom domain is added in Railway dashboard
3. Check Cloudflare SSL mode is "Full" (not "Flexible")
4. Ensure DNS is pointing to correct Railway URL

### Apple OAuth Redirect Mismatch

**Problem**: `redirect_uri_mismatch` error

**Solutions**:
1. Verify callback URL in Apple Developer Portal matches exactly:
   - Must be: `https://pr.manajet.io/auth/apple/callback`
   - No trailing slash
   - Must use HTTPS
2. Check Service ID configuration is saved
3. Wait 5-10 minutes after updating Apple settings

### Railway Deployment Issues

**Problem**: App not deploying or showing errors

**Solutions**:
1. Check build logs: `railway logs`
2. Verify environment variables are set: `railway variables`
3. Ensure requirements.txt is complete
4. Check Railway dashboard for build errors

## Quick Reference

### Current Configuration

- **Service ID**: `io.manajet.connect10`
- **Production Domain**: `pr.manajet.io`
- **Callback URL**: `https://pr.manajet.io/auth/apple/callback`
- **Hosting**: Railway

### DNS Record Template

```
Type: CNAME
Name: pr
Value: [your-railway-app].up.railway.app
TTL: Auto/300
```

### Required Apple OAuth URLs

```
Domain: pr.manajet.io
Return URL: https://pr.manajet.io/auth/apple/callback
```

## Next Steps

1. ✅ Configure DNS records for pr.manajet.io
2. ✅ Add custom domain in Railway
3. ✅ Wait for SSL certificate provisioning
4. ✅ Update Apple Developer Portal with production callback URL
5. ✅ Test the complete OAuth flow
6. ✅ Monitor logs for any issues

## Support Resources

- **Railway Docs**: https://docs.railway.app/deploy/deployments
- **Cloudflare DNS**: https://developers.cloudflare.com/dns/
- **Apple Sign In**: https://developer.apple.com/sign-in-with-apple/

## Security Checklist

- [ ] DNS records configured correctly
- [ ] SSL certificate active (HTTPS working)
- [ ] Apple OAuth callback URL matches production domain
- [ ] Environment variables set in production
- [ ] SECRET_KEY is different from development
- [ ] DEBUG=False in production
- [ ] SESSION_COOKIE_SECURE=True
- [ ] No sensitive credentials in code repository
