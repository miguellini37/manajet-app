#!/usr/bin/env python3
"""
Generate Apple Client Secret for Sign in with Apple OAuth

This script generates a JWT token that serves as the client secret for Apple OAuth.
The token is valid for 180 days (Apple's maximum).

You'll need:
1. Team ID: Already filled in below (6B3HT757P9)
2. Key ID: Get from https://developer.apple.com/account/resources/authkeys/list
3. Private Key (.p8 file): Downloaded when you created the key (can only download once!)
"""

import jwt
import time
from pathlib import Path

# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

# Your Apple Developer Team ID (already filled in)
TEAM_ID = "6B3HT757P9"

# Your Service ID (already configured)
CLIENT_ID = "io.manajet.connect10"

# Your Apple Sign in with Apple Key ID
KEY_ID = "8654CCS94G"

# Your downloaded private key file
KEY_FILE = "AuthKey_8654CCS94G.p8"

# ============================================================================
# GENERATE CLIENT SECRET
# ============================================================================

def generate_client_secret():
    """Generate Apple OAuth client secret (JWT token)"""

    # Check if key file exists
    if not Path(KEY_FILE).exists():
        print(f"ERROR: Private key file not found: {KEY_FILE}")
        print("\nPlease:")
        print("1. Download your .p8 private key from Apple Developer Portal")
        print("2. Place it in the same directory as this script")
        print("3. Update the KEY_FILE variable above with the correct filename")
        return None

    # Check if KEY_ID is still placeholder
    if KEY_ID == "YOUR_KEY_ID_HERE":
        print("ERROR: KEY_ID is still set to placeholder value")
        print("\nPlease:")
        print("1. Go to: https://developer.apple.com/account/resources/authkeys/list")
        print("2. Find your key and copy the Key ID (10 characters)")
        print("3. Update the KEY_ID variable in this script")
        return None

    # Read the private key
    with open(KEY_FILE, 'r') as f:
        private_key = f.read()

    # JWT headers
    headers = {
        "kid": KEY_ID,
        "alg": "ES256"
    }

    # JWT payload
    # Token valid for 180 days (15,552,000 seconds) - Apple's maximum
    current_time = int(time.time())
    expiration_time = current_time + (86400 * 180)  # 180 days

    payload = {
        "iss": TEAM_ID,                              # Issuer (your Team ID)
        "iat": current_time,                         # Issued at
        "exp": expiration_time,                      # Expires (180 days)
        "aud": "https://appleid.apple.com",          # Audience (Apple)
        "sub": CLIENT_ID                             # Subject (your Service ID)
    }

    # Generate the JWT
    client_secret = jwt.encode(
        payload,
        private_key,
        algorithm="ES256",
        headers=headers
    )

    return client_secret, expiration_time


def main():
    print("=" * 70)
    print("Apple Client Secret Generator for Manajet")
    print("=" * 70)
    print()
    print("Configuration:")
    print(f"  Team ID:     {TEAM_ID}")
    print(f"  Client ID:   {CLIENT_ID}")
    print(f"  Key ID:      {KEY_ID}")
    print(f"  Key File:    {KEY_FILE}")
    print()
    print("-" * 70)
    print()

    # Generate the secret
    result = generate_client_secret()

    if result is None:
        print("\nFailed to generate client secret. Please fix the errors above.")
        return

    client_secret, expiration_time = result

    # Calculate expiration date
    from datetime import datetime
    exp_date = datetime.fromtimestamp(expiration_time)

    print("SUCCESS! Client Secret Generated")
    print("=" * 70)
    print()
    print("Your Apple Client Secret (JWT Token):")
    print()
    print(client_secret)
    print()
    print("-" * 70)
    print()
    print(f"Valid until: {exp_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"(Expires in 180 days - set a reminder to regenerate!)")
    print()
    print("=" * 70)
    print()
    print("NEXT STEPS:")
    print()
    print("1. Copy the token above (the long string)")
    print()
    print("2. Add it to DigitalOcean environment variables:")
    print("   - Go to: https://cloud.digitalocean.com/apps")
    print("   - Click your 'manajet' app")
    print("   - Settings tab → App-Level Environment Variables")
    print("   - Click 'Edit'")
    print("   - Find APPLE_CLIENT_SECRET (or add new variable)")
    print("   - Paste the token")
    print("   - Mark as 'Encrypted' (lock icon)")
    print("   - Click 'Save'")
    print()
    print("3. DigitalOcean will automatically redeploy (takes 2-3 minutes)")
    print()
    print("4. Configure Apple Developer Portal:")
    print("   - Go to: https://developer.apple.com/account/resources/identifiers/list/serviceId")
    print("   - Click 'io.manajet.connect10'")
    print("   - Check 'Sign in with Apple'")
    print("   - Click 'Configure'")
    print("   - Add domain: pr.manajet.io")
    print("   - Add return URL: https://pr.manajet.io/auth/apple/callback")
    print("   - Click 'Save' → 'Continue' → 'Save'")
    print()
    print("5. Test Sign in with Apple at: https://pr.manajet.io")
    print()
    print("=" * 70)
    print()
    print("SECURITY NOTES:")
    print("  - Keep this token secret (like a password)")
    print("  - Don't commit it to git")
    print("  - Set a calendar reminder to regenerate in 6 months")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nMake sure you have installed required packages:")
        print("  pip install pyjwt cryptography")
