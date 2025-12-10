# Deployment Steps for Apple Sign In

## Option 1: SSH into Production Server (Recommended)

If your production backend is on DigitalOcean, Railway, or another server:

```bash
# 1. SSH into your production server
ssh your-server

# 2. Navigate to your app directory
cd /path/to/manajet-app

# 3. Pull the latest changes
git pull origin main

# 4. Activate virtual environment (if using one)
source venv/bin/activate

# 5. Install new dependencies
pip install -r requirements.txt

# 6. Run the migration script
python migrate_add_apple_user_id.py

# 7. Restart your application
# For systemd:
sudo systemctl restart manajet

# For PM2:
pm2 restart manajet

# For Docker:
docker-compose restart
```

## Option 2: Direct SQL Migration

If you prefer to run SQL directly on your database:

```bash
# Connect to your PostgreSQL database
psql -h your-db-host -U your-db-user -d your-db-name

# Run the SQL file
\i add_apple_user_id.sql

# Or copy-paste the SQL commands:
```

```sql
ALTER TABLE users ADD COLUMN apple_user_id VARCHAR(255);
ALTER TABLE users ADD CONSTRAINT users_apple_user_id_unique UNIQUE (apple_user_id);
CREATE INDEX idx_users_apple_user_id ON users(apple_user_id);
```

## Option 3: Using Database GUI (TablePlus, pgAdmin, etc.)

1. Connect to your production database
2. Open the SQL console
3. Run the contents of `add_apple_user_id.sql`

## Verify Migration

After running the migration, verify it worked:

```sql
-- Check if column exists
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'users'
AND column_name = 'apple_user_id';

-- Should return:
-- column_name    | data_type
-- ---------------+-----------
-- apple_user_id  | character varying
```

## Deploy Backend Code

```bash
# On your production server
cd ~/manajet-app
git pull origin main
pip install -r requirements.txt
# Restart your application server
```

## Test the Integration

1. Build and run your iOS app
2. Tap "Sign in with Apple"
3. Complete authentication
4. Check your database:

```sql
SELECT user_id, username, email, apple_user_id
FROM users
WHERE apple_user_id IS NOT NULL;
```

## Rollback (if needed)

If you need to rollback the changes:

```sql
-- Remove the column
ALTER TABLE users DROP COLUMN apple_user_id;
```

## Production Checklist

- [ ] Database migration completed
- [ ] Backend code deployed
- [ ] Application server restarted
- [ ] iOS app built with Apple Sign In capability
- [ ] Apple Developer Portal configured
- [ ] Tested sign-in flow
- [ ] Verified user creation in database
- [ ] Tested logout and re-login
