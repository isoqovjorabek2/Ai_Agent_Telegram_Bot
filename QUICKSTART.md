# Quick Start Guide

Get your Telegram bot running in 10 minutes!

## Prerequisites

- Python 3.8 or higher
- Google Cloud account
- Telegram account

## Step 1: Create Telegram Bot (2 minutes)

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token (looks like: `123456:ABC-DEF...`)

## Step 2: Setup Google OAuth (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable APIs:
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search and enable: **Google Calendar API**
   - Search and enable: **Google Tasks API**
4. Create OAuth credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen first
   - Application type: **Web application**
   - Name: `Telegram Bot`
   - Authorized redirect URIs: `http://localhost:3000/callback.html`
   - Click "Create"
5. Copy **Client ID** and **Client Secret**

## Step 3: Install & Configure (3 minutes)

1. **Clone/Download the project**
```bash
cd /path/to/project
```

2. **Run setup script**
```bash
bash setup.sh
```

3. **Edit .env file**
```bash
nano .env
```

Add your credentials:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
BACKEND_URL=http://localhost:8000
WEBAPP_URL=http://localhost:3000
REDIRECT_URI=http://localhost:3000/callback.html
```

Save and exit (Ctrl+X, Y, Enter)

## Step 4: Start Services (1 minute)

Open **3 terminal windows**:

### Terminal 1 - Backend
```bash
cd backend
source ../venv/bin/activate
uvicorn app:app --reload
```

### Terminal 2 - Webapp
```bash
cd webapp
python3 -m http.server 3000
```

### Terminal 3 - Bot
```bash
cd telegram-bot
source ../venv/bin/activate
python3 bot.py
```

## Step 5: Test It! (1 minute)

1. Open Telegram and find your bot
2. Send `/start`
3. Click "Sign in with Google"
4. Authorize the app
5. Send a message: `Ertaga soat 14:00 da doktor`
6. Check your Google Calendar! 🎉

## Common Commands

```bash
/start   - Start the bot
/help    - Show help
/auth    - Connect Google account
/status  - Check connection status
```

## Example Messages

**Calendar events:**
- `Ertaga soat 14:00 da doktor` (Uzbek)
- `Завтра в 15:30 встреча` (Russian)
- `Dushanba kuni 10 da yig'ilish`

**Notes:**
- `Non va sut sotib olish`
- `Eslatma: kitob o'qish`
- `Заметка: купить хлеб`

## Troubleshooting

### "Backend bilan aloqa yo'q"
- Make sure backend is running on port 8000
- Check BACKEND_URL in .env

### "OAuth errors"
- Verify redirect URI in Google Console matches exactly
- Make sure APIs are enabled

### Bot doesn't respond
- Check if bot token is correct
- Verify bot service is running
- Look at terminal logs for errors

## Next Steps

- **Production Deployment:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Customize:** Edit handlers in `telegram-bot/handlers.py`
- **Add Features:** Check backend endpoints in `backend/app.py`

## Need Help?

- Check logs in terminal windows
- Read full [README.md](README.md)
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

Enjoy your bot! 🤖