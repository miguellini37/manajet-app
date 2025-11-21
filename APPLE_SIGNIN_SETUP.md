# Sign in with Apple Setup Guide

This guide will help you complete the Apple OAuth integration for Manajet.

## Prerequisites

You've already registered your Service ID: **io.manajet.connect10**

## Apple Developer Portal Configuration

### 1. Create an App ID (if not done already)

1. Go to [Apple Developer Portal](https://developer.apple.com/account/)
2. Navigate to "Certificates, Identifiers & Profiles"
3. Click "Identifiers" → "+ "Add
4. Select "App IDs" → Continue
5. Fill in:
   - Description: "Manajet Web App"
   - Bundle ID: `io.manajet.webapp` (or your preferred bundle ID)
   - Capabilities: Check "Sign in with Apple"
6. Click "Register"

### 2. Configure your Service ID

1. Go to "Identifiers" in Apple Developer Portal
2. Click your Service ID: **io.manajet.connect10**
3. Check "Sign in with Apple"
4. Click "Configure" next to "Sign in with Apple"
5. Configure the following:
   - **Primary App ID**: Select the App ID you created above
   - **Domains and Subdomains**: Add both:
     - `pr.manajet.io` (production)
     - `localhost:5000` (development - if testing locally)
   - **Return URLs**: Add both callback URLs:
     - For local development: `http://localhost:5000/auth/apple/callback`
     - For production: `https://pr.manajet.io/auth/apple/callback`

6. Click "Save" → "Continue" → "Register"

**Important**: You must add BOTH URLs for development and production to work. Apple requires exact matches.

### 3. Create a Private Key

1. Go to "Keys" in Apple Developer Portal
2. Click "+" to create a new key
3. Configure:
   - **Key Name**: "Manajet Sign in with Apple Key"
   - Check "Sign in with Apple"
   - Click "Configure" → Select your Primary App ID
4. Click "Continue" → "Register"
5. **IMPORTANT**: Download the `.p8` private key file
   - You can only download this ONCE
   - Save it securely (e.g., `AuthKey_XXXXXXXXXX.p8`)
6. Note the **Key ID** (e.g., `XXXXXXXXXX`)

### 4. Get Your Team ID

1. Go to [Apple Developer Membership](https://developer.apple.com/account/#!/membership/)
2. Copy your **Team ID** (10-character identifier)

## Generate Client Secret

Apple requires a JWT client secret. You'll need to generate this using your private key.

### Option 1: Use Python Script

Create a file `generate_apple_secret.py`:

```python
import jwt
import time

# Configuration (update these values)
TEAM_ID = "YOUR_TEAM_ID"  # From Apple Developer Membership page
CLIENT_ID = "io.manajet.connect10"  # Your Service ID
KEY_ID = "YOUR_KEY_ID"  # From the key you created
KEY_FILE = "AuthKey_XXXXXXXXXX.p8"  # Path to your downloaded .p8 file

# Read the private key
with open(KEY_FILE, 'r') as f:
    private_key = f.read()

# Generate the JWT
headers = {
    "kid": KEY_ID,
    "alg": "ES256"
}

payload = {
    "iss": TEAM_ID,
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400 * 180,  # 180 days (max allowed)
    "aud": "https://appleid.apple.com",
    "sub": CLIENT_ID
}

client_secret = jwt.encode(
    payload,
    private_key,
    algorithm="ES256",
    headers=headers
)

print(f"Client Secret (valid for 180 days):")
print(client_secret)
```

Run it:
```bash
pip install pyjwt cryptography
python generate_apple_secret.py
```

### Option 2: Use Online Generator

Use a trusted JWT generator with ES256 algorithm support. **WARNING**: Only use for testing, not production.

## Environment Configuration

### 1. Create/Update `.env` file

Add these variables to your `.env` file:

```env
# Sign in with Apple
APPLE_CLIENT_ID=io.manajet.connect10
APPLE_CLIENT_SECRET=your_generated_jwt_token_here
```

### 2. Update for Production

For Railway or other production deployments, set these environment variables:

```bash
railway variables set APPLE_CLIENT_ID="io.manajet.connect10"
railway variables set APPLE_CLIENT_SECRET="your_generated_jwt_token_here"
```

## Testing the Integration

### Local Testing

1. Start your Flask app: `python web_app.py`
2. Navigate to: `http://localhost:5000/login`
3. Click "Sign in with Apple"
4. You should be redirected to Apple's login page
5. After successful login, you'll be redirected back to your app

### Production Testing

1. Deploy your app to your production domain
2. Ensure your callback URL matches what you configured in Apple Developer Portal
3. Test the complete flow

## Troubleshooting

### Common Issues

1. **"invalid_client" error**
   - Check that your Client Secret JWT is valid and not expired
   - Verify APPLE_CLIENT_ID matches your Service ID exactly
   - Regenerate the client secret if it's been > 180 days

2. **"redirect_uri_mismatch" error**
   - Ensure the callback URL in Apple Developer Portal matches exactly
   - Check for trailing slashes
   - Verify the domain is correct

3. **"invalid_grant" error**
   - User may have canceled the authentication
   - Try the flow again

4. **No email returned**
   - Apple only sends email/name data on the FIRST sign-in
   - For testing, go to Apple ID settings and remove Manajet app access
   - Sign in again to get email data

## Security Notes

- **Never commit** your `.p8` private key file to version control
- **Never commit** your Client Secret to version control
- Store sensitive keys in environment variables or secure vaults
- Regenerate Client Secret every 180 days (Apple's maximum)
- Use HTTPS in production (required by Apple)

## Support

- Apple Developer Documentation: https://developer.apple.com/sign-in-with-apple/
- Apple WWDC Sessions: Search for "Sign in with Apple"
- Authlib Documentation: https://docs.authlib.org/

## Renewal Schedule

Client Secrets are valid for a maximum of 180 days. Set a reminder to regenerate your secret before expiration.

**Current Secret Expiration**: [Calculate from creation date]
**Renewal Due Date**: [180 days from creation]
