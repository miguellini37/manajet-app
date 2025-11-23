# Deploy Apple Sign In to DigitalOcean

## Quick Deployment Steps

### Step 1: Add Database Column (2 minutes)

You have two options:

#### **Option A: Using DigitalOcean Database Console** (Easiest)

1. Go to [DigitalOcean Console](https://cloud.digitalocean.com/)
2. Click **Databases** in left menu
3. Select your PostgreSQL database
4. Click **Users & Databases** tab
5. Click **Open Console** button (or **Connection Details** → **Connection String**)
6. In the SQL console, run:

```sql
ALTER TABLE users ADD COLUMN apple_user_id VARCHAR(255);
ALTER TABLE users ADD CONSTRAINT users_apple_user_id_unique UNIQUE (apple_user_id);
CREATE INDEX idx_users_apple_user_id ON users(apple_user_id);
```

7. Verify:
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'apple_user_id';
```

#### **Option B: SSH to Droplet**

```bash
# SSH into your droplet
ssh root@pr.manajet.io

# Connect to database
psql $DATABASE_URL

# Run the migration SQL
ALTER TABLE users ADD COLUMN apple_user_id VARCHAR(255);
ALTER TABLE users ADD CONSTRAINT users_apple_user_id_unique UNIQUE (apple_user_id);
CREATE INDEX idx_users_apple_user_id ON users(apple_user_id);
```

### Step 2: Deploy Backend Code (3 minutes)

```bash
# SSH into your droplet
ssh root@pr.manajet.io

# Navigate to your app directory
cd /var/www/manajet-app  # or wherever your app is

# Pull latest changes
git pull origin main

# Install new dependencies
pip3 install -r requirements.txt
# or if using virtual environment:
source venv/bin/activate && pip install -r requirements.txt

# Restart your application
systemctl restart manajet
# or
systemctl restart gunicorn
# or check what service name you're using:
systemctl list-units --type=service | grep -E 'manajet|gunicorn|flask'
```

### Step 3: Verify Deployment

```bash
# Check if service is running
systemctl status manajet  # or your service name

# Check logs
journalctl -u manajet -f --lines=50

# Test the endpoint
curl -X POST https://pr.manajet.io/api/auth/apple \
  -H "Content-Type: application/json" \
  -d '{"identity_token": "test", "user_identifier": "test"}'

# Should return error (expected) but confirms endpoint exists
```

### Step 4: Test from iOS App

1. Open Xcode
2. Build and run ManajetPR app
3. Tap "Sign in with Apple"
4. Complete authentication
5. Verify you're logged in

## Troubleshooting

### If you don't know your SSH details:

```bash
# Check your DigitalOcean droplet
# Go to: https://cloud.digitalocean.com/droplets
# Click your droplet → Access tab
# Use the console or copy the SSH command
```

### If you don't know your app directory:

```bash
# SSH into droplet
ssh root@pr.manajet.io

# Find your app
find /var -name "web_app.py" 2>/dev/null
# or
find /home -name "web_app.py" 2>/dev/null
# or
ls -la /var/www/
ls -la /home/
```

### If you don't know your service name:

```bash
# List all running services
systemctl list-units --type=service | grep -E 'manajet|gunicorn|flask|python'

# Check what's listening on port 5000 or 8000
netstat -tlnp | grep -E ':5000|:8000'
```

### If git pull fails (uncommitted changes):

```bash
# Stash changes
git stash

# Pull
git pull origin main

# Or force pull (be careful!)
git fetch origin
git reset --hard origin/main
```

## Complete Deployment Checklist

- [ ] Database column added (verify with SQL query)
- [ ] Backend code pulled from git
- [ ] Python dependencies installed
- [ ] Application service restarted
- [ ] Service is running (check systemctl status)
- [ ] Logs show no errors
- [ ] Endpoint responds (test with curl)
- [ ] iOS app can sign in with Apple
- [ ] New user created in database
- [ ] Dashboard loads after login

## Quick Reference Commands

```bash
# SSH to server
ssh root@pr.manajet.io

# Navigate to app
cd /var/www/manajet-app

# Update code
git pull origin main

# Restart service
systemctl restart manajet

# Check status
systemctl status manajet

# View logs
journalctl -u manajet -f
```

## Need Help?

If you get stuck, share:
1. The error message
2. Output of: `systemctl status [your-service-name]`
3. Recent logs: `journalctl -u [your-service-name] -n 50`
