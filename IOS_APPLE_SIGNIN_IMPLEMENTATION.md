# iOS Apple Sign In Implementation Guide

## Overview

Complete implementation of Sign in with Apple for the Manajet iOS app, including both frontend (iOS app) and backend (Flask API) components.

## What Was Implemented

### iOS App (ManajetPR)

#### 1. **AppleSignInCoordinator.swift** (New)
- Location: `ManajetPR/ManajetPR/Services/AppleSignInCoordinator.swift`
- Handles native iOS Sign in with Apple authentication flow
- Manages authorization requests and responses
- Extracts identity token and user information

#### 2. **LoginView.swift** (Updated)
- Added native "Sign in with Apple" button
- Integrated with SwiftUI's `SignInWithAppleButton`
- Added divider between traditional and Apple sign-in methods
- Implemented async authentication handling

#### 3. **APIClient.swift** (Updated)
- Added `loginWithApple()` method
- Sends identity token to backend endpoint: `POST /api/auth/apple`
- Handles user creation and session management

### Backend (Flask)

#### 1. **web_app.py** (Updated)
- Added `/api/auth/apple` endpoint for iOS native authentication
- Validates Apple identity tokens
- Creates or retrieves users based on Apple user identifier
- Automatically creates customer accounts for new users
- Manages session creation

#### 2. **db_models.py** (Updated)
- Added `apple_user_id` column to `UserModel`
- Indexed for fast lookups
- Unique constraint to prevent duplicate Apple accounts

#### 3. **migrate_add_apple_user_id.py** (New)
- Database migration script
- Safely adds `apple_user_id` column to existing databases
- Checks if column exists before adding

## Setup Instructions

### Step 1: Enable Sign in with Apple in Xcode

1. Open `ManajetPR.xcodeproj` in Xcode
2. Select the ManajetPR target
3. Go to "Signing & Capabilities" tab
4. Click "+ Capability"
5. Add "Sign in with Apple"

### Step 2: Configure Apple Developer Portal

1. Go to [Apple Developer Portal](https://developer.apple.com/account)
2. Navigate to "Certificates, Identifiers & Profiles"
3. Select your app identifier: `io.manajet.ManajetPR`
4. Enable "Sign in with Apple" capability
5. Save your changes

### Step 3: Run Database Migration

For existing production databases, add the `apple_user_id` column:

```bash
cd ~/manajet-app
python migrate_add_apple_user_id.py
```

The script will:
- Add `apple_user_id VARCHAR(255) UNIQUE` column to users table
- Create an index on the column
- Check if column exists to prevent errors on re-run

### Step 4: Deploy Backend Changes

Deploy the updated backend to production:

```bash
# Commit changes
git add web_app.py db_models.py migrate_add_apple_user_id.py
git commit -m "Add iOS native Apple Sign In support"
git push origin main

# Deploy to production (DigitalOcean/Railway)
# Your deployment process here
```

### Step 5: Test the Integration

1. Build and run the iOS app
2. Tap "Sign in with Apple" on the login screen
3. Complete Apple authentication
4. Verify user is created and logged in
5. Check dashboard loads correctly

## How It Works

### Authentication Flow

```
┌─────────────┐
│   iOS App   │
└──────┬──────┘
       │ 1. User taps "Sign in with Apple"
       ▼
┌─────────────────────────┐
│  Apple Authentication   │
│   (Face ID/Touch ID)    │
└──────────┬──────────────┘
           │ 2. Returns identity token
           ▼
┌─────────────────────────┐
│    iOS App Receives     │
│   - identity_token      │
│   - user_identifier     │
│   - email (first time)  │
│   - name (first time)   │
└──────────┬──────────────┘
           │ 3. POST to /api/auth/apple
           ▼
┌─────────────────────────┐
│   Flask Backend         │
│   - Validates token     │
│   - Creates/finds user  │
│   - Creates session     │
└──────────┬──────────────┘
           │ 4. Returns success
           ▼
┌─────────────────────────┐
│    iOS App              │
│   - Fetches user data   │
│   - Shows dashboard     │
└─────────────────────────┘
```

### First Sign-In vs. Subsequent Sign-Ins

**First Sign-In:**
- Apple provides: identity_token, user_identifier, email, full_name
- Backend creates new customer account
- Backend creates new user account
- Stores apple_user_id for future logins

**Subsequent Sign-Ins:**
- Apple provides: identity_token, user_identifier (no email/name)
- Backend looks up user by apple_user_id
- Backend creates session
- User is authenticated

## API Endpoint Details

### POST /api/auth/apple

**Request Body:**
```json
{
  "identity_token": "eyJraWQiOiJXNldjT0tC...",
  "user_identifier": "001234.abcd1234efgh5678.9012",
  "email": "user@example.com",
  "full_name": {
    "given_name": "John",
    "family_name": "Doe"
  }
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful"
}
```

**Error Response (401/400/500):**
```json
{
  "success": false,
  "message": "Error description"
}
```

## Database Schema

### users Table (Updated)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | VARCHAR(50) | PRIMARY KEY | User ID |
| username | VARCHAR(100) | UNIQUE, NOT NULL | Username |
| password_hash | VARCHAR(255) | NOT NULL | Password hash (set to "apple_oauth" for Apple users) |
| role | VARCHAR(50) | NOT NULL | User role |
| related_id | VARCHAR(50) | | Links to customer_id |
| email | VARCHAR(200) | | User email |
| **apple_user_id** | **VARCHAR(255)** | **UNIQUE** | **Apple user identifier** |
| created_at | TIMESTAMP | | Creation timestamp |
| updated_at | TIMESTAMP | | Update timestamp |

## Security Considerations

### Token Validation

The current implementation decodes the identity token without full signature verification for development purposes. For production:

1. **Fetch Apple's public keys:**
```python
import requests

def get_apple_public_keys():
    response = requests.get('https://appleid.apple.com/auth/keys')
    return response.json()
```

2. **Verify the token signature:**
```python
from jwt import decode, PyJWKClient

jwks_client = PyJWKClient('https://appleid.apple.com/auth/keys')
signing_key = jwks_client.get_signing_key_from_jwt(identity_token)

decoded = decode(
    identity_token,
    signing_key.key,
    algorithms=["RS256"],
    audience=APPLE_CLIENT_ID,
    issuer="https://appleid.apple.com"
)
```

### Session Security

- Sessions are marked as permanent for persistence
- Sessions use secure cookies in production (HTTPS required)
- Sessions expire after configured lifetime (default: 1 hour)

### User Privacy

- Respects "Hide My Email" feature (stores relay email)
- Only receives email/name on first sign-in
- Stores minimal user information

## Troubleshooting

### Issue: "Invalid token" error

**Cause:** Identity token is malformed or expired

**Solution:**
- Tokens expire after 10 minutes
- Make sure network requests are fast
- Ensure backend receives token quickly

### Issue: User not created

**Cause:** Database migration not run or username conflict

**Solution:**
- Run `migrate_add_apple_user_id.py`
- Check backend logs for specific error
- Verify database has apple_user_id column

### Issue: Sign in button doesn't appear

**Cause:** Missing capability in Xcode

**Solution:**
- Add "Sign in with Apple" capability
- Clean build folder (Cmd+Shift+K)
- Rebuild project

### Issue: "Column 'apple_user_id' doesn't exist"

**Cause:** Database migration not run

**Solution:**
```bash
python migrate_add_apple_user_id.py
```

## Testing Checklist

- [ ] Sign in with Apple button appears on login screen
- [ ] Tapping button shows Apple authentication sheet
- [ ] Successful authentication creates new user
- [ ] User data is correctly stored in database
- [ ] Session is created and persists
- [ ] Dashboard loads after authentication
- [ ] Logout works correctly
- [ ] Subsequent sign-ins work without re-entering info
- [ ] "Hide My Email" feature works

## Additional Features to Consider

1. **Account Linking:** Allow users to link existing username/password accounts with Apple ID
2. **Token Refresh:** Implement token refresh for long-lived sessions
3. **Revocation Handling:** Handle when users revoke Apple Sign In access
4. **Multi-device Support:** Ensure seamless experience across devices

## Support Resources

- [Apple Sign In Documentation](https://developer.apple.com/sign-in-with-apple/)
- [Apple REST API Docs](https://developer.apple.com/documentation/sign_in_with_apple/sign_in_with_apple_rest_api)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)

## Deployment Notes

### Production Deployment

1. Ensure HTTPS is enabled (required by Apple)
2. Verify Apple Developer Portal configuration
3. Run database migration on production database
4. Test with production Apple ID credentials
5. Monitor logs for any authentication errors

### Environment Variables

No additional environment variables needed for iOS native authentication (only for web OAuth).

## Files Modified/Created

### iOS App
- ✅ `ManajetPR/ManajetPR/Services/AppleSignInCoordinator.swift` (New)
- ✅ `ManajetPR/ManajetPR/Views/LoginView.swift` (Updated)
- ✅ `ManajetPR/ManajetPR/Services/APIClient.swift` (Updated)

### Backend
- ✅ `web_app.py` (Updated - added /api/auth/apple endpoint)
- ✅ `db_models.py` (Updated - added apple_user_id column)
- ✅ `migrate_add_apple_user_id.py` (New)

### Documentation
- ✅ `APPLE_SIGN_IN_SETUP.md` (in iOS project)
- ✅ `IOS_APPLE_SIGNIN_IMPLEMENTATION.md` (this file)
