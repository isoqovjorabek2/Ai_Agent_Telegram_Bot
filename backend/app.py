from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

from auth import get_google_credentials, initiate_oauth_flow, handle_oauth_callback
from google_calendar import create_calendar_event, get_user_calendars
from notes import create_keep_note
from db import get_user_tokens, save_user_tokens, delete_user_tokens, init_db

app = FastAPI(title="Telegram Bot Backend")

# ---------------- CORS Middleware ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Startup ----------------
@app.on_event("startup")
async def startup_event():
    init_db()

# ---------------- Models ----------------
class OAuthInitiate(BaseModel):
    user_id: int

class OAuthCallback(BaseModel):
    code: str
    user_id: int

class CalendarEventCreate(BaseModel):
    user_id: int
    title: str
    datetime: str  # ISO format
    description: Optional[str] = ""

class NoteCreate(BaseModel):
    user_id: int
    title: str
    content: Optional[str] = ""

# ---------------- Root ----------------
@app.get("/")
async def root():
    return {"status": "ok", "service": "telegram-bot-backend"}

# ---------------- AUTH ----------------
@app.post("/api/auth/initiate")
async def initiate_auth(data: OAuthInitiate):
    """Initiate OAuth flow"""
    try:
        auth_url = initiate_oauth_flow(data.user_id)
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/callback")
async def auth_callback(data: OAuthCallback):
    """Handle OAuth callback (POST)"""
    try:
        result = handle_oauth_callback(data.code, data.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/oauth/callback")
async def oauth_callback(code: str, state: str):
    """Handle OAuth callback (GET)"""
    try:
        user_id = int(state)
        result = handle_oauth_callback(code, user_id)

        # Pretty success HTML
        return HTMLResponse(content=f"""
        <html>
            <head>
                <title>Authentication Successful</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f0f0f0;
                    }}
                    .container {{
                        text-align: center;
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .success {{
                        color: #4CAF50;
                        font-size: 24px;
                        margin-bottom: 20px;
                    }}
                    .email {{
                        color: #666;
                        margin-bottom: 20px;
                    }}
                    .message {{
                        color: #333;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success">✓ Authentication Successful!</div>
                    <div class="email">Authenticated as: {result['email']}</div>
                    <div class="message">You can now close this window and return to Telegram.</div>
                </div>
            </body>
        </html>
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/auth/status/{user_id}")
async def auth_status(user_id: int):
    """Check if user is authenticated"""
    tokens = get_user_tokens(user_id)

    if not tokens:
        return {"authenticated": False}

    # ✅ FIX: check for either 'token' or 'access_token'
    token_value = tokens.get('token') or tokens.get('access_token')
    expiry_str = tokens.get('expiry')

    if not token_value:
        return {"authenticated": False}

    # Optional: Check expiry time if stored
    if expiry_str:
        try:
            expiry = datetime.fromisoformat(expiry_str)
            if expiry < datetime.now(timezone.utc):
                return {"authenticated": False, "expired": True}
        except Exception:
            pass

    return {"authenticated": True, "email": tokens.get('email', 'N/A')}


@app.delete("/api/auth/revoke/{user_id}")
async def revoke_auth(user_id: int):
    """Revoke user authentication"""
    try:
        delete_user_tokens(user_id)
        return {"status": "revoked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- CALENDAR ----------------
@app.post("/api/calendar/create")
async def create_event(data: CalendarEventCreate):
    """Create a Google Calendar event"""
    try:
        creds = get_google_credentials(data.user_id)
        if not creds:
            raise HTTPException(status_code=401, detail="User not authenticated")

        event_datetime = datetime.fromisoformat(data.datetime)

        event = create_calendar_event(
            creds,
            title=data.title,
            start_time=event_datetime,
            description=data.description
        )

        return {
            "status": "created",
            "event_id": event.get('id'),
            "link": event.get('htmlLink')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/calendar/list/{user_id}")
async def list_calendars(user_id: int):
    """List user's calendars"""
    try:
        creds = get_google_credentials(user_id)
        if not creds:
            raise HTTPException(status_code=401, detail="User not authenticated")

        calendars = get_user_calendars(creds)
        return {"calendars": calendars}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- NOTES ----------------
@app.post("/api/notes/create")
async def create_note(data: NoteCreate):
    """Create Google Keep note"""
    try:
        creds = get_google_credentials(data.user_id)
        if not creds:
            raise HTTPException(status_code=401, detail="User not authenticated")

        note = create_keep_note(
            creds,
            title=data.title,
            content=data.content
        )

        return {
            "status": "created",
            "note_id": note.get('name')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- Run ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
