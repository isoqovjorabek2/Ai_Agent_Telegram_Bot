import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from db import get_user_tokens, save_user_tokens

# OAuth 2.0 scopes
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/keep"
]

CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [os.getenv("REDIRECT_URI")]
    }
}


def initiate_oauth_flow(user_id: int) -> str:
    """
    Initiate OAuth flow and return authorization URL
    """
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=CLIENT_CONFIG['web']['redirect_uris'][0]
    )

    # Generate authorization URL with state parameter
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=str(user_id),  # Use user_id as state
        prompt='consent'  # Force consent to get refresh token
    )

    return authorization_url


def handle_oauth_callback(code: str, user_id: int) -> dict:
    """
    Handle OAuth callback and save tokens
    """
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=CLIENT_CONFIG['web']['redirect_uris'][0]
    )

    # Exchange authorization code for tokens
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Save tokens to database
    tokens = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': list(credentials.scopes),
        'expiry': credentials.expiry.isoformat() if credentials.expiry else None
    }

    # Get user email & profile info
    from googleapiclient.discovery import build
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    tokens['email'] = user_info.get('email')

    save_user_tokens(user_id, tokens)

    return {
        "status": "success",
        "email": tokens['email']
    }


def get_google_credentials(user_id: int) -> Credentials:
    """
    Get Google credentials for user, refresh if needed
    """
    tokens = get_user_tokens(user_id)

    if not tokens:
        return None

    # Check if scopes match — if not, force re-auth
    saved_scopes = set(tokens.get('scopes', []))
    required_scopes = set(SCOPES)
    if saved_scopes != required_scopes:
        print("⚠️ Scope mismatch, user must re-authenticate.")
        return None

    creds = Credentials(
        token=tokens.get('token'),
        refresh_token=tokens.get('refresh_token'),
        token_uri=tokens.get('token_uri'),
        client_id=tokens.get('client_id'),
        client_secret=tokens.get('client_secret'),
        scopes=tokens.get('scopes')
    )

    # Refresh token if expired
    if creds.refresh_token:
        try:
            if creds.expired or not creds.valid:
                creds.refresh(Request())
                # Update tokens in database
                tokens['token'] = creds.token
                tokens['expiry'] = creds.expiry.isoformat() if creds.expiry else None
                save_user_tokens(user_id, tokens)
        except Exception as e:
            print(f"Token refresh error: {e}")
            return None

    return creds
