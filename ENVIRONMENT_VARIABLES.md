# 🔐 Environment Variables Configuration Guide

This document outlines all environment variables needed to run the Telegram Bot system across different components.

## 📦 Component Overview

The system consists of three main components:
1. **Backend API** (FastAPI - deployed to Heroku/Railway/etc.)
2. **Webapp** (Static HTML/JS - deployed to Vercel)
3. **Telegram Bot** (Python bot - deployed with backend or separately)

---

## 🎯 Backend API Environment Variables

Deploy location: Heroku, Railway, Render, or any Python hosting platform

### Required Variables:

#### 1. `TELEGRAM_BOT_TOKEN` ⚠️ **CRITICAL**
- **Description**: Your Telegram bot token from @BotFather
- **How to get**: 
  1. Open Telegram and search for `@BotFather`
  2. Send `/newbot` or use existing bot with `/mybots`
  3. Get the token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
- **Example**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### 2. `GOOGLE_CLIENT_ID` ⚠️ **CRITICAL**
- **Description**: Google OAuth 2.0 Client ID
- **How to get**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com)
  2. Create a new project or select existing
  3. Enable Google Calendar API and Google Keep API
  4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
  5. Application type: "Web application"
  6. Add authorized redirect URIs (see below)
- **Example**: `123456789-abcdefghijklmnop.apps.googleusercontent.com`

#### 3. `GOOGLE_CLIENT_SECRET` ⚠️ **CRITICAL**
- **Description**: Google OAuth 2.0 Client Secret (paired with Client ID)
- **How to get**: Shown when you create the OAuth client ID
- **Example**: `GOCSPX-abcdefghijklmnop123456789`

#### 4. `WEBAPP_URL` ⚠️ **CRITICAL**
- **Description**: The URL where your webapp is deployed (Vercel)
- **Example**: `https://your-project.vercel.app`
- **Note**: No trailing slash

#### 5. `REDIRECT_URI` ⚠️ **CRITICAL**
- **Description**: OAuth callback URL (must match Google Cloud Console)
- **Example**: `https://your-project.vercel.app/callback.html`
- **Formula**: `{WEBAPP_URL}/callback.html`

#### 6. `BACKEND_URL` (Optional for backend)
- **Description**: Your backend API URL (for self-reference)
- **Example**: `https://your-backend.herokuapp.com`
- **Note**: No trailing slash

#### 7. `DB_PATH` (Optional)
- **Description**: SQLite database file path
- **Default**: `telegram_bot.db`
- **Note**: For production, consider PostgreSQL instead

### Google Cloud Console Configuration:

In your Google OAuth 2.0 Client, add these **Authorized redirect URIs**:
```
https://your-project.vercel.app/callback.html
http://localhost:3000/callback.html  (for local testing)
```

And these **Authorized JavaScript origins**:
```
https://your-project.vercel.app
http://localhost:3000  (for local testing)
```

---

## 🌐 Webapp Environment Variables (Vercel)

Deploy location: Vercel

### Required Variables:

#### 1. `BACKEND_URL` ⚠️ **CRITICAL**
- **Description**: URL of your deployed backend API
- **Example**: `https://your-backend.herokuapp.com`
- **Purpose**: Webapp makes API calls to this URL for OAuth and calendar operations
- **Note**: No trailing slash

### How to Set in Vercel:

**Via Vercel Dashboard:**
1. Go to your project in Vercel
2. Settings → Environment Variables
3. Add `BACKEND_URL` with your backend URL
4. Apply to: Production, Preview, Development

**Via Vercel CLI:**
```bash
vercel env add BACKEND_URL
# Enter your backend URL when prompted
```

---

## 🤖 Local Development Setup

For local development, create a `.env` file in the root directory:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret

# Local URLs
BACKEND_URL=http://localhost:8000
WEBAPP_URL=http://localhost:3000
REDIRECT_URI=http://localhost:3000/callback.html

# Database
DB_PATH=telegram_bot.db
```

---

## 📋 Quick Setup Checklist

### Step 1: Create Google OAuth Credentials
- [ ] Go to Google Cloud Console
- [ ] Create OAuth 2.0 Client ID (Web application)
- [ ] Note down Client ID and Client Secret
- [ ] Add redirect URIs

### Step 2: Create Telegram Bot
- [ ] Talk to @BotFather on Telegram
- [ ] Create new bot or use existing
- [ ] Get bot token

### Step 3: Deploy Backend
- [ ] Deploy backend to Heroku/Railway/Render
- [ ] Set environment variables:
  - `TELEGRAM_BOT_TOKEN`
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `WEBAPP_URL` (will set after Step 4)
  - `REDIRECT_URI` (will set after Step 4)

### Step 4: Deploy Webapp
- [ ] Deploy webapp to Vercel
- [ ] Set environment variable:
  - `BACKEND_URL` (from Step 3)
- [ ] Get Vercel URL

### Step 5: Update Configuration
- [ ] Update backend's `WEBAPP_URL` with Vercel URL
- [ ] Update backend's `REDIRECT_URI` with `{Vercel_URL}/callback.html`
- [ ] Update Google OAuth redirect URIs with Vercel callback URL

### Step 6: Test
- [ ] Open Telegram bot
- [ ] Try authentication flow
- [ ] Verify OAuth works end-to-end

---

## 🔍 Environment Variables Summary Table

| Variable | Component | Required | Example | Purpose |
|----------|-----------|----------|---------|---------|
| `TELEGRAM_BOT_TOKEN` | Backend | ✅ | `123:ABC...` | Telegram bot authentication |
| `GOOGLE_CLIENT_ID` | Backend | ✅ | `123.apps.googleusercontent.com` | Google OAuth |
| `GOOGLE_CLIENT_SECRET` | Backend | ✅ | `GOCSPX-abc...` | Google OAuth |
| `WEBAPP_URL` | Backend | ✅ | `https://app.vercel.app` | Frontend URL |
| `REDIRECT_URI` | Backend | ✅ | `https://app.vercel.app/callback.html` | OAuth callback |
| `BACKEND_URL` | Webapp | ✅ | `https://api.herokuapp.com` | Backend API URL |
| `DB_PATH` | Backend | ⚪ | `telegram_bot.db` | Database path |

Legend: ✅ Required | ⚪ Optional

---

## 🐛 Troubleshooting

### Issue: OAuth redirect doesn't work
**Check:**
- Google Console redirect URIs match exactly
- `REDIRECT_URI` in backend matches Google Console
- `WEBAPP_URL` in backend points to correct Vercel deployment

### Issue: Webapp can't connect to backend
**Check:**
- `BACKEND_URL` in Vercel is set correctly
- Backend is deployed and running
- CORS is configured in backend to allow Vercel domain

### Issue: Telegram bot doesn't respond
**Check:**
- `TELEGRAM_BOT_TOKEN` is correct
- Backend is deployed and running
- Bot process is running

---

## 🔒 Security Notes

1. **Never commit** `.env` files or expose environment variables in code
2. **Use HTTPS** for all production URLs
3. **Rotate secrets** periodically
4. **Limit OAuth scopes** to only what's needed
5. **Configure CORS** properly in backend

---

## 📚 Additional Resources

- [Vercel Environment Variables Docs](https://vercel.com/docs/environment-variables)
- [Google OAuth 2.0 Setup](https://developers.google.com/identity/protocols/oauth2)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Heroku Config Vars](https://devcenter.heroku.com/articles/config-vars)

---

**Questions?** Check the deployment documentation:
- `webapp/VERCEL_DEPLOYMENT.md` - Webapp deployment guide
- `DEPLOYMENT.md` - Full system deployment guide
