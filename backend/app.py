from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime

# Support both running as a package (uvicorn backend.app:app) and as a script (python app.py)
try:
    from .auth import (
        get_google_credentials,
        initiate_oauth_flow,
        handle_oauth_callback,
    )
    from .google_calendar import create_calendar_event, get_user_calendars
    from .notes import create_keep_note
    from .db import (
        get_user_tokens,
        save_user_tokens,
        delete_user_tokens,
        init_db,
    )
except ImportError:  # pragma: no cover - fallback for script execution
    # Ensure local directory is importable when running as a script
    import sys as _sys
    _sys.path.append(os.path.dirname(__file__))
    from auth import (
        get_google_credentials,
        initiate_oauth_flow,
        handle_oauth_callback,
    )
    from google_calendar import create_calendar_event, get_user_calendars
    from notes import create_keep_note
    from db import get_user_tokens, save_user_tokens, delete_user_tokens, init_db

app = FastAPI(title="Telegram Bot Backend")

# CORS middleware (configurable via env CORS_ORIGINS="http://localhost:3000,https://yourdomain")
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
allow_origins = (
    [o.strip() for o in cors_origins_env.split(",") if o.strip()]
    if cors_origins_env != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Serve static webapp under /webapp
WEBAPP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "webapp"))
if os.path.isdir(WEBAPP_DIR):
    app.mount("/webapp", StaticFiles(directory=WEBAPP_DIR, html=True), name="webapp")

# Pydantic models
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

# Health check
@app.get("/")
async def root():
    return {"status": "ok", "service": "telegram-bot-backend"}

# Auth endpoints
@app.post("/api/auth/initiate")
async def initiate_auth(data: OAuthInitiate):
    """Initiate OAuth flow"""
    try:
        auth_url = initiate_oauth_flow(data.user_id)
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Convenience GET endpoint to start OAuth via redirect (useful for simple clients)
@app.get("/auth/google")
async def auth_google_redirect(user_id: int):
    try:
        auth_url = initiate_oauth_flow(user_id)
        return RedirectResponse(url=auth_url, status_code=302)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/callback")
async def auth_callback(data: OAuthCallback):
    """Handle OAuth callback"""
    try:
        result = handle_oauth_callback(data.code, data.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve OAuth callback page at a clean path that can be used in Google Console
@app.get("/oauth/callback")
async def oauth_callback_page():
    callback_file = os.path.join(WEBAPP_DIR, "callback.html")
    if os.path.isfile(callback_file):
        return FileResponse(callback_file)
    return {"status": "missing_callback_page"}

@app.get("/api/auth/status/{user_id}")
async def auth_status(user_id: int):
    """Check if user is authenticated"""
    tokens = get_user_tokens(user_id)
    
    if tokens and 'access_token' in tokens:
        return {
            "authenticated": True,
            "email": tokens.get('email', 'N/A')
        }
    
    return {"authenticated": False}

@app.delete("/api/auth/revoke/{user_id}")
async def revoke_auth(user_id: int):
    """Revoke user authentication"""
    try:
        delete_user_tokens(user_id)
        return {"status": "revoked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Calendar endpoints
@app.post("/api/calendar/create")
async def create_event(data: CalendarEventCreate):
    """Create calendar event"""
    try:
        # Get user credentials
        creds = get_google_credentials(data.user_id)
        if not creds:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        # Parse datetime
        event_datetime = datetime.fromisoformat(data.datetime)
        
        # Create event
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

# Notes endpoints
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)