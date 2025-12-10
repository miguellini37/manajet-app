-- Migration: Add apple_user_id column to users table
-- Run this SQL script directly on your production database

-- Check if column exists first (PostgreSQL)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'users'
        AND column_name = 'apple_user_id'
    ) THEN
        -- Add the column
        ALTER TABLE users ADD COLUMN apple_user_id VARCHAR(255);

        -- Make it unique
        ALTER TABLE users ADD CONSTRAINT users_apple_user_id_unique UNIQUE (apple_user_id);

        -- Add index for faster lookups
        CREATE INDEX idx_users_apple_user_id ON users(apple_user_id);

        RAISE NOTICE 'Successfully added apple_user_id column';
    ELSE
        RAISE NOTICE 'Column apple_user_id already exists';
    END IF;
END $$;
