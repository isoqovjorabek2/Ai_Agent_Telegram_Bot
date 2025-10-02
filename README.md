# Telegram Bot with Google Calendar & Keep Integration

A Telegram bot that understands Uzbek and Russian natural language to create Google Calendar events and Google Keep notes.

## Features

- 🇺🇿 **Uzbek Language Support** - Understands natural Uzbek commands
- 🇷🇺 **Russian Language Support** - Understands natural Russian commands
- 📅 **Google Calendar** - Automatically creates calendar events
- 📝 **Google Keep/Tasks** - Creates notes and tasks
- 🔐 **Secure OAuth** - Google authentication via OAuth 2.0
- 🤖 **Smart Parsing** - Natural language processing for dates and times

## Project Structure

```
/telegram-bot
   bot.py              # Main Telegram bot
   handlers.py         # NLP parser for Uzbek/Russian
/backend
   app.py              # FastAPI server
   auth.py             # Google OAuth flow
   calendar.py         # Google Calendar integration
   notes.py            # Google Keep/Tasks integration
   db.py               # SQLite database logic
/webapp
   index.html          # OAuth sign-in page
   oauth.js            # OAuth client-side logic
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Telegram Bot Token

### 2. Create Telegram Bot

1. Open Telegram and find [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow instructions
3. Save your bot token

### 3. Setup Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs:
   - Google Calendar API
   - Google Tasks API (or Keep API if available)
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:3000/oauth/callback`
   - Save Client ID and Client Secret

### 4. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Fill in:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `GOOGLE_CLIENT_ID` - From Google Cloud Console
- `GOOGLE_CLIENT_SECRET` - From Google Cloud Console
- Other URLs (keep defaults for local development)

### 6. Initialize Database

```bash
cd backend
python db.py
```

### 7. Run the Application

Open 3 terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
# Or with uvicorn:
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Webapp:**
```bash
cd webapp
# Serve with any static file server
python -m http.server 3000
# Or use: npx serve -p 3000
```

**Terminal 3 - Telegram Bot:**
```bash
cd telegram-bot
python bot.py
```

## Usage

### 1. Start the Bot

Open Telegram and find your bot, then send `/start`

### 2. Connect Google Account

Click the "Google bilan kirish / Войти через Google" button and authorize access

### 3. Send Messages

The bot understands natural language in Uzbek and Russian:

**Calendar Examples:**
- `Ertaga soat 14:00 da doktor` → Creates calendar event tomorrow at 2 PM
- `Завтра в 15:30 встреча` → Creates meeting tomorrow at 3:30 PM
- `Dushanba kuni 10 da yig'ilish` → Creates event on Monday at 10 AM
- `25 dekabr soat 18:00 da bozor` → Creates event on Dec 25 at 6 PM

**Notes Examples:**
- `Non va sut sotib olish` → Creates shopping list note
- `Eslatma: kitob o'qish` → Creates reminder note
- `Заметка: купить хлеб` → Creates note
- `Не забыть позвонить` → Creates task

## Commands

- `/start` - Start bot and check authentication
- `/help` - Show help message
- `/auth` - Re-authenticate with Google
- `/status` - Check connection status

## NLP Features

The bot can parse:

### Time Formats
- `soat 14`, `в 14:00`, `14:30`, `14.30`

### Date Keywords

**Uzbek:**
- `bugun` (today), `ertaga` (tomorrow), `indinga` (day after)
- `dushanba, seshanba, chorshanba, payshanba, juma, shanba, yakshanba`

**Russian:**
- `сегодня` (today), `завтра` (tomorrow), `послезавтра` (day after)
- `понедельник, вторник, среда, четверг, пятница, суббота, воскресенье`

### Specific Dates
- `25 dekabr`, `15 yanvar`
- `25 декабря`, `15 января`

## API Endpoints

### Authentication
- `POST /api/auth/initiate` - Start OAuth flow
- `POST /api/auth/callback` - Handle OAuth callback
- `GET /api/auth/status/{user_id}` - Check auth status
- `DELETE /api/auth/revoke/{user_id}` - Revoke access

### Calendar
- `POST /api/calendar/create` - Create event
- `GET /api/calendar/list/{user_id}` - List calendars

### Notes
- `POST /api/notes/create` - Create note

## Database Schema

```sql
-- Users and their OAuth tokens
users (user_id, email, tokens, created_at, updated_at)

-- Cached events
events (id, user_id, event_id, title, start_time, created_at)

-- Cached notes
notes (id, user_id, note_id, title, content, created_at)

-- User preferences
preferences (user_id, language, timezone, notifications)
```

## Security Notes

- OAuth tokens are stored encrypted in SQLite database
- Never commit `.env` file to version control
- Use HTTPS in production
- Rotate credentials regularly
- Set proper CORS origins in production

## Production Deployment

### Backend (Railway, Heroku, DigitalOcean)
1. Set environment variables
2. Update `BACKEND_URL` to your domain
3. Enable HTTPS
4. Set proper CORS origins

### Webapp (Vercel, Netlify, GitHub Pages)
1. Deploy static files
2. Update `REDIRECT_URI` in Google Cloud Console
3. Update `WEBAPP_URL` in environment

### Bot
1. Run on VPS or cloud server
2. Use process manager (pm2, systemd)
3. Enable logging

## Troubleshooting

**Bot not responding:**
- Check if bot token is correct
- Verify backend is running
- Check firewall/network settings

**OAuth errors:**
- Verify Client ID and Secret
- Check redirect URI matches exactly
- Ensure APIs are enabled in Google Cloud

**Database errors:**
- Run `python db.py` to initialize
- Check file permissions

**Keep API not available:**
- Keep API is not officially public
- Bot uses Google Tasks API as fallback
- For unofficial Keep access, uncomment gkeepapi in code

## Contributing

Feel free to open issues or submit pull requests!

## License

MIT License - feel free to use and modify as needed.

## Support

For questions or issues:
- Open a GitHub issue
- Contact: isoqovjorabek774@gmail.com
