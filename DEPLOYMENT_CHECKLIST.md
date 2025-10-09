# 🚀 Deployment Checklist - Google Sign-In Integration

## ✅ Prerequisites Completed

- [x] Backend OAuth endpoints implemented (`/api/auth/initiate`, `/api/auth/callback`)
- [x] Frontend OAuth flow implemented (webapp/oauth.js, webapp/callback.html)
- [x] Database schema for user tokens storage created
- [x] Telegram bot integration with webapp URL
- [x] Merge conflicts resolved
- [x] Auth status endpoint bug fixed (token vs access_token)
- [x] Default redirect URI fixed in backend

---

## 🔧 Environment Variables Setup

### Backend Environment Variables (Render/Heroku/Railway)

Required environment variables for backend deployment:

```bash
# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Google OAuth Credentials (from Google Cloud Console)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_client_secret

# Webapp URL (your Vercel deployment URL)
WEBAPP_URL=https://your-project.vercel.app

# OAuth Redirect URI (must match Google Console)
REDIRECT_URI=https://your-project.vercel.app/callback.html

# Optional: Backend URL (for self-reference)
BACKEND_URL=https://your-backend.render.com
```

### Webapp Environment Variables (Vercel)

Required environment variable for Vercel deployment:

```bash
# Backend API URL (your backend deployment URL)
ENV_BACKEND_URL=https://your-backend.render.com
```

**How to set in Vercel:**
1. Go to your Vercel project dashboard
2. Settings → Environment Variables
3. Add `ENV_BACKEND_URL` with your backend URL
4. Apply to: Production, Preview, Development

Or via CLI:
```bash
vercel env add ENV_BACKEND_URL
```

---

## 📋 Google Cloud Console Configuration

1. **Go to** [Google Cloud Console](https://console.cloud.google.com)
2. **Select your project** or create a new one
3. **Enable APIs:**
   - Google Calendar API
   - Google Tasks API
   - (Google Keep API is not public, using Tasks instead)

4. **Create OAuth 2.0 Credentials:**
   - Go to: APIs & Services → Credentials
   - Click: Create Credentials → OAuth 2.0 Client ID
   - Application type: **Web application**
   
5. **Configure OAuth Client:**
   
   **Authorized JavaScript origins:**
   ```
   https://your-project.vercel.app
   http://localhost:3000
   ```
   
   **Authorized redirect URIs:**
   ```
   https://your-project.vercel.app/callback.html
   http://localhost:3000/callback.html
   ```

6. **Save credentials:**
   - Copy Client ID → use in backend `GOOGLE_CLIENT_ID`
   - Copy Client Secret → use in backend `GOOGLE_CLIENT_SECRET`

---

## 🔄 Deployment Steps

### Step 1: Deploy Backend

**Using Render.com (recommended):**
```bash
# 1. Connect your GitHub repo to Render
# 2. Create new Web Service
# 3. Settings:
#    - Build Command: pip install -r backend/requirements.txt
#    - Start Command: cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
#    - Root Directory: /
```

**Set environment variables in Render:**
- TELEGRAM_BOT_TOKEN
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- WEBAPP_URL (set after Step 2)
- REDIRECT_URI (set after Step 2)

### Step 2: Deploy Webapp

**Using Vercel:**
```bash
# From webapp directory
cd webapp
vercel

# Or deploy via Vercel dashboard by connecting GitHub repo
```

**Set environment variable in Vercel:**
```bash
vercel env add ENV_BACKEND_URL
# Enter your backend URL from Step 1
```

### Step 3: Update Configuration

1. **Update Backend Environment Variables:**
   - Set `WEBAPP_URL` to your Vercel deployment URL
   - Set `REDIRECT_URI` to `https://your-vercel-url.vercel.app/callback.html`

2. **Update Google Cloud Console:**
   - Go to OAuth 2.0 Client settings
   - Add your Vercel URL to Authorized JavaScript origins
   - Add `https://your-vercel-url.vercel.app/callback.html` to Authorized redirect URIs

### Step 4: Deploy Telegram Bot

The bot can run alongside the backend or separately:

**Option A: Run with Backend (on Render):**
```bash
# In Render dashboard, add Background Worker:
# Command: cd telegram-bot && python bot.py
```

**Option B: Separate deployment:**
```bash
# Deploy to another service with same environment variables
python telegram-bot/bot.py
```

---

## 🧪 Testing the Integration

### 1. Test Webapp Direct Access
```bash
# Open in browser:
https://your-project.vercel.app?user_id=123456

# You should see:
# - Google Sign-In button
# - Clicking should redirect to Google OAuth
```

### 2. Test OAuth Flow
1. Click "Sign in with Google"
2. Authorize the application
3. Should redirect to callback.html
4. Should show success message with email

### 3. Test Telegram Bot
```bash
# In Telegram:
/start
# Should show Google sign-in button if not authenticated

# Click the button
# Should open webapp with user_id parameter

# After authentication
/status
# Should show authenticated status with email
```

### 4. Test Calendar Integration
```bash
# In Telegram (after authentication):
"Ertaga soat 14:00 da doktor"
# Should create calendar event

/help
# Should show all available commands
```

---

## 🔍 Verification Checklist

- [ ] Backend is deployed and accessible
- [ ] Webapp is deployed and accessible
- [ ] Environment variables are set correctly:
  - [ ] Backend: TELEGRAM_BOT_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, WEBAPP_URL, REDIRECT_URI
  - [ ] Webapp: ENV_BACKEND_URL
- [ ] Google Cloud Console configured:
  - [ ] OAuth 2.0 credentials created
  - [ ] Redirect URIs match deployment URLs
  - [ ] Required APIs enabled
- [ ] Telegram bot is running
- [ ] OAuth flow works end-to-end
- [ ] Calendar event creation works
- [ ] Note creation works

---

## 🐛 Common Issues & Solutions

### Issue 1: "OAuth redirect doesn't work"
**Solution:**
- Verify redirect URI in Google Console matches **exactly**: `https://your-app.vercel.app/callback.html`
- Check `REDIRECT_URI` in backend matches Google Console
- Ensure `WEBAPP_URL` points to correct Vercel deployment

### Issue 2: "Webapp can't connect to backend"
**Solution:**
- Verify `ENV_BACKEND_URL` is set in Vercel
- Check backend is deployed and running
- Verify CORS is enabled in backend (already configured)

### Issue 3: "Backend returns 401 Unauthorized"
**Solution:**
- Verify Google OAuth credentials are correct
- Check user has completed OAuth flow
- Verify tokens are saved in database

### Issue 4: "Telegram bot doesn't respond"
**Solution:**
- Check `TELEGRAM_BOT_TOKEN` is correct
- Verify bot process is running
- Check backend API is accessible

### Issue 5: "env.js not loading properly"
**Solution:**
- Verify build script runs: `bash build-env.sh`
- Check `/api/env.js` serverless function works
- Verify `ENV_BACKEND_URL` is set in Vercel

---

## 📊 Architecture Overview

```
User (Telegram) 
    ↓
Telegram Bot (/start) 
    ↓
Checks auth status (Backend API)
    ↓
If not authenticated → Shows button with webapp URL
    ↓
User clicks button → Opens Webapp
    ↓
Webapp loads → Calls Backend /api/auth/initiate
    ↓
Backend returns Google OAuth URL
    ↓
User authenticates with Google
    ↓
Google redirects to → Webapp/callback.html
    ↓
Callback sends code to → Backend /api/auth/callback
    ↓
Backend exchanges code for tokens → Saves to database
    ↓
User returns to Telegram → Now authenticated
    ↓
User sends message → Bot creates calendar/note via Backend API
```

---

## 🎯 Next Steps After Deployment

1. **Monitor logs** for any errors
2. **Test with real users** in Telegram
3. **Set up error tracking** (optional: Sentry, LogRocket)
4. **Enable HTTPS** (should be automatic with Vercel/Render)
5. **Consider database migration** from SQLite to PostgreSQL for production
6. **Set up automated backups** for user data

---

## 📚 Related Documentation

- [ENVIRONMENT_VARIABLES.md](./ENVIRONMENT_VARIABLES.md) - Detailed environment variables guide
- [webapp/VERCEL_DEPLOYMENT.md](./webapp/VERCEL_DEPLOYMENT.md) - Vercel-specific deployment
- [webapp/README.md](./webapp/README.md) - Webapp documentation
- [README.md](./README.md) - Main project documentation

---

## ✅ Deployment Complete!

Once all checkboxes are marked, your application is ready for production use!

**Support:**
- Backend: FastAPI running on Render/Heroku/Railway
- Webapp: Static HTML/JS on Vercel
- Bot: Python Telegram bot on Render/separate service
- Database: SQLite (consider PostgreSQL for production)
