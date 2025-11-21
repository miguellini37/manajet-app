"""
OAuth Configuration for Social Login
Supports Sign in with Apple, Google, etc.
"""

import os
from authlib.integrations.flask_client import OAuth

# Initialize OAuth
oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth providers"""
    oauth.init_app(app)

    # Apple Sign In
    if os.environ.get('APPLE_CLIENT_ID'):
        oauth.register(
            name='apple',
            client_id=os.environ.get('APPLE_CLIENT_ID'),
            client_secret=os.environ.get('APPLE_CLIENT_SECRET'),
            server_metadata_url='https://appleid.apple.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'name email'
            }
        )

    # Google Sign In
    if os.environ.get('GOOGLE_CLIENT_ID'):
        oauth.register(
            name='google',
            client_id=os.environ.get('GOOGLE_CLIENT_ID'),
            client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )

    return oauth
