# Deployment Guide

This guide covers deploying the Telegram Bot to various platforms.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [Railway Deployment](#railway-deployment)
4. [VPS/Cloud Server](#vps-deployment)
5. [Environment Variables](#environment-variables)

---

## Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Google OAuth credentials configured
- Telegram bot token

### Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-directory>
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

3. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

4. **Check logs**
```bash
docker-compose logs -f
```

5. **Stop services**
```bash
docker-compose down
```

---

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Heroku account

### Backend Deployment

1. **Create Heroku app**
```bash
heroku create your-bot-backend
```

2. **Set environment variables**
```bash
heroku config:set GOOGLE_CLIENT_ID=your_client_id
heroku config:set GOOGLE_CLIENT_SECRET=your_client_secret
heroku config:set REDIRECT_URI=https://your-webapp.herokuapp.com/callback.html
```

3. **Deploy backend**
```bash
git push heroku main
```

### Bot Deployment

1. **Create separate app for bot**
```bash
heroku create your-telegram-bot
```

2. **Set environment variables**
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token
heroku config:set BACKEND_URL=https://your-bot-backend.herokuapp.com
heroku config:set WEBAPP_URL=https://your-webapp.herokuapp.com
```

3. **Scale worker**
```bash
heroku ps:scale web=0 bot=1
```

### Webapp Deployment

Deploy to Vercel, Netlify, or GitHub Pages (see below).

---

## Railway Deployment

### Prerequisites
- Railway account
- Railway CLI (optional)

### Steps

1. **Go to [Railway.app](https://railway.app)**

2. **Create New Project**
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Add Environment Variables**
   - Go to Variables tab
   - Add all required environment variables

4. **Deploy**
   - Railway will automatically deploy
   - Get your backend URL from the deployment

---

## VPS Deployment

### Prerequisites
- Ubuntu/Debian VPS
- Domain name (optional)
- SSH access

### Steps

1. **Connect to VPS**
```bash
ssh user@your-server-ip
```

2. **Install dependencies**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx
```

3. **Clone repository**
```bash
cd /opt
sudo git clone <your-repo-url> telegram-bot
cd telegram-bot
```

4. **Setup Python environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

5. **Configure environment**
```bash
cp .env.example .env
nano .env
```

6. **Initialize database**
```bash
cd backend && python3 db.py && cd ..
```

7. **Setup systemd services**

Create `/etc/systemd/system/telegram-bot-backend.service`:
```ini
[Unit]
Description=Telegram Bot Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/telegram-bot/backend
Environment="PATH=/opt/telegram-bot/venv/bin"
ExecStart=/opt/telegram-bot/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/telegram-bot/telegram-bot
Environment="PATH=/opt/telegram-bot/venv/bin"
ExecStart=/opt/telegram-bot/venv/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

8. **Start services**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot-backend
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot-backend
sudo systemctl start telegram-bot
```

9. **Setup Nginx for webapp**

Create `/etc/nginx/sites-available/telegram-bot-webapp`:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /opt/telegram-bot/webapp;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/telegram-bot-webapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

10. **Setup SSL with Let's Encrypt (optional)**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Webapp Deployment (Vercel/Netlify)

### Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
cd webapp
vercel
```

3. **Set environment variables**
   - Go to Vercel dashboard
   - Add environment variable: `ENV_BACKEND_URL=https://your-backend.com`

### Netlify

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Deploy**
```bash
cd webapp
netlify deploy --prod
```

3. **Configure**
   - Update `config.js` with production backend URL

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | `123456:ABC-DEF...` |
| `GOOGLE_CLIENT_ID` | OAuth client ID | `xxxxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret | `GOCSPX-xxxxx` |
| `BACKEND_URL` | Backend API URL | `https://api.example.com` |
| `WEBAPP_URL` | Webapp URL | `https://example.com` |
| `REDIRECT_URI` | OAuth redirect URI | `https://example.com/callback.html` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_PATH` | Database file path | `telegram_bot.db` |

---

## Post-Deployment Checklist

- [ ] Update Google OAuth redirect URIs in Google Cloud Console
- [ ] Test OAuth flow end-to-end
- [ ] Verify bot responds in Telegram
- [ ] Test calendar event creation
- [ ] Test note creation
- [ ] Setup monitoring/logging
- [ ] Configure backups for database
- [ ] Enable HTTPS
- [ ] Update CORS origins in production

---

## Troubleshooting

### Bot not responding
- Check bot token is correct
- Verify backend URL is accessible
- Check bot service logs

### OAuth errors
- Verify redirect URI matches exactly
- Check Google Cloud Console credentials
- Ensure APIs are enabled

### Database errors
- Check file permissions
- Verify DB_PATH is writable
- Run database initialization

---

## Monitoring

### Health Checks

Backend health endpoint:
```bash
curl https://your-backend.com/
```

### Logs

View backend logs:
```bash
sudo journalctl -u telegram-bot-backend -f
```

View bot logs:
```bash
sudo journalctl -u telegram-bot -f
```

---

## Security Best Practices

1. **Never commit .env file**
2. **Use environment variables for secrets**
3. **Enable HTTPS in production**
4. **Regularly rotate credentials**
5. **Set proper CORS origins**
6. **Keep dependencies updated**
7. **Enable rate limiting**
8. **Monitor logs for suspicious activity**

---

## Support

For issues or questions, please open an issue on GitHub.