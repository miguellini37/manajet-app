# Namecheap DNS Setup for pr.manajet.io

This guide shows exactly how to configure your DNS in Namecheap for the production domain pr.manajet.io.

## Prerequisites

- You own the domain `manajet.io` on Namecheap
- You have Railway deployment URL (from `railway domain` command)

## Step-by-Step Instructions

### 1. Log into Namecheap

1. Go to https://www.namecheap.com/
2. Click "Sign In" (top right)
3. Enter your credentials

### 2. Access Domain Management

1. Click **"Domain List"** in the left sidebar
2. Find **"manajet.io"** in your list of domains
3. Click the **"Manage"** button next to it

### 3. Navigate to Advanced DNS

1. You'll see tabs at the top: Details, Sharing & Transfer, etc.
2. Click the **"Advanced DNS"** tab
3. You should see a list of DNS records (if any exist)

### 4. Add the CNAME Record

#### First, get your Railway URL

If you haven't deployed yet, do this first:
```bash
railway up
railway domain
```

Copy the URL (e.g., `manajet-production.up.railway.app`)

#### Now add the CNAME record:

1. Scroll down to **"Host Records"** section
2. Click the **"Add New Record"** button
3. Fill in the form:

   | Field | Value |
   |-------|-------|
   | **Type** | Select "CNAME Record" from dropdown |
   | **Host** | `pr` |
   | **Value** | `your-railway-app.up.railway.app` (paste your Railway URL) |
   | **TTL** | Select "Automatic" or "1 min" |

4. Click the **green checkmark** (✓) button to save

### Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│ Advanced DNS                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ HOST RECORDS                                            │
│                                                         │
│ ┌──────┬──────┬────────────────────────┬─────┬───┐   │
│ │ Type │ Host │ Value                  │ TTL │ ✓ │   │
│ ├──────┼──────┼────────────────────────┼─────┼───┤   │
│ │CNAME │ pr   │ manajet-prod.up.rail...│Auto │ ✓ │   │
│ └──────┴──────┴────────────────────────┴─────┴───┘   │
│                                                         │
│ [+ ADD NEW RECORD]                                      │
└─────────────────────────────────────────────────────────┘
```

### 5. Verify the Record

After saving, you should see your new record in the list:

```
Type: CNAME
Host: pr
Value: your-railway-app.up.railway.app
TTL: Automatic
```

### 6. Wait for Propagation

- **Namecheap propagation time**: Usually 5-30 minutes
- **Global propagation**: Can take up to 24 hours (but usually much faster)

Check propagation status:
```bash
# Check if DNS is working (wait 5-10 minutes first)
nslookup pr.manajet.io

# Or use online tool:
# https://www.whatsmydns.net/#CNAME/pr.manajet.io
```

## Common Namecheap Issues

### Issue 1: "Host already exists"

**Problem**: You already have a record with host "pr"

**Solution**:
1. Find the existing "pr" record
2. Click the trash icon (🗑️) to delete it
3. Add the new CNAME record

### Issue 2: Wrong record type

**Problem**: You added an A record instead of CNAME

**Solution**:
1. Delete the A record
2. Add a new record with Type = "CNAME Record"

### Issue 3: Value has "http://" or "https://"

**Problem**: You included the protocol in the value

**Solution**:
- ❌ Wrong: `https://manajet-prod.up.railway.app`
- ✅ Correct: `manajet-prod.up.railway.app`

### Issue 4: DNS not resolving after 30 minutes

**Solution**:
1. Check you saved the record (green checkmark)
2. Verify "Host" is exactly `pr` (not `pr.manajet.io`)
3. Try flushing your DNS cache:
   ```bash
   # Windows
   ipconfig /flushdns
   ```
4. Try using Google DNS (8.8.8.8) to check

## Next Steps After DNS is Configured

### 1. Add Custom Domain in Railway

```bash
railway domain pr.manajet.io
```

Railway will:
- Detect your DNS is configured correctly
- Generate an SSL certificate (5-10 minutes)
- Enable HTTPS automatically

### 2. Test Your Domain

After SSL is ready (10-15 minutes):

```bash
# Should return 200 OK
curl -I https://pr.manajet.io
```

Or visit in browser: https://pr.manajet.io

### 3. Configure Apple Sign In

Once pr.manajet.io is loading:

1. Go to Apple Developer Portal
2. Add domain: `pr.manajet.io`
3. Add callback: `https://pr.manajet.io/auth/apple/callback`

## Quick Reference

### Your Configuration
- **Domain**: `manajet.io`
- **Subdomain**: `pr`
- **Full URL**: `pr.manajet.io`
- **Record Type**: CNAME
- **Points to**: `[your-railway-app].up.railway.app`

### Namecheap DNS Settings Location
1. Namecheap Dashboard
2. Domain List
3. Manage (next to manajet.io)
4. Advanced DNS tab
5. Host Records section

## Troubleshooting Commands

```bash
# Check if DNS is resolving
nslookup pr.manajet.io

# Check DNS from Google's servers
nslookup pr.manajet.io 8.8.8.8

# Check detailed DNS info
dig pr.manajet.io

# Test HTTPS connection
curl -I https://pr.manajet.io

# Check Railway domain status
railway status
```

## Support

- **Namecheap Support**: https://www.namecheap.com/support/
- **Namecheap DNS Guide**: https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-cname-record-for-my-domain/
- **Railway Support**: https://railway.app/help

## Completion Checklist

- [ ] Logged into Namecheap
- [ ] Found manajet.io domain
- [ ] Clicked "Advanced DNS" tab
- [ ] Added CNAME record: pr → railway-url
- [ ] Clicked green checkmark to save
- [ ] Verified record appears in list
- [ ] Waited 10-15 minutes
- [ ] Tested with `nslookup pr.manajet.io`
- [ ] Added custom domain in Railway
- [ ] SSL certificate generated (another 10 minutes)
- [ ] Tested https://pr.manajet.io loads

## Estimated Time

- **Adding DNS record**: 2 minutes
- **DNS propagation**: 5-30 minutes
- **SSL certificate**: 5-10 minutes after DNS works
- **Total**: 15-45 minutes

Most of this is waiting - you can work on Apple OAuth configuration while waiting!
