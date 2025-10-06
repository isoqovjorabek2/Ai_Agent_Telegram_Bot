# Vercel Deployment Guide

Deploy the webapp to Vercel with serverless functions for environment variables.

## 🚀 Quick Deploy

### Option 1: One-Click Deploy (Easiest)

1. Click this button:
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_REPO_URL&project-name=telegram-bot-webapp&env=ENV_BACKEND_URL)

2. Set environment variable:
   - `ENV_BACKEND_URL` = Your backend URL (e.g., `https://your-backend.herokuapp.com`)

3. Done! ✅

### Option 2: Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from webapp directory**
   ```bash
   cd webapp
   vercel
   ```

4. **Set environment variables**
   ```bash
   vercel env add ENV_BACKEND_URL
   # Enter your backend URL when prompted
   ```

5. **Deploy to production**
   ```bash
   vercel --prod
   ```

### Option 3: Vercel Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Select the `webapp` folder as root directory
5. Add environment variable:
   - **Name:** `ENV_BACKEND_URL`
   - **Value:** Your backend URL (e.g., `https://api.yourapp.com`)
6. Click "Deploy"

---

## 🔧 How It Works

### Serverless Function for Environment Variables

The webapp uses Vercel serverless functions to inject environment variables:

```javascript
// webapp/api/env.js
export default function handler(req, res) {
  res.setHeader("Content-Type", "application/javascript");
  const backendUrl = process.env.ENV_BACKEND_URL || "http://localhost:8000";
  res.send(`window.ENV_BACKEND_URL = "${backendUrl}";`);
}
```

### Loading in HTML

```html
<!-- Load environment from serverless function -->
<script src="/api/env.js"></script>
<!-- Then load your app -->
<script src="config.js"></script>
<script src="oauth.js"></script>
```

This ensures environment variables are:
- ✅ Never hardcoded in frontend
- ✅ Configurable per environment (dev/staging/prod)
- ✅ Secure (managed in Vercel dashboard)

---

## 📁 Project Structure

```
webapp/
├── api/
│   └── env.js              # Serverless function for env vars
├── index.html              # Main OAuth page
├── callback.html           # OAuth callback handler
├── oauth.js                # OAuth logic
├── config.js               # Configuration management
├── vercel.json             # Vercel configuration
├── package.json            # Project metadata
└── .vercelignore           # Files to ignore
```

---

## 🔐 Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV_BACKEND_URL` | Backend API URL | `https://api.yourapp.com` |

---

## 🌍 Custom Domain (Optional)

1. Go to your project in Vercel
2. Settings → Domains
3. Add your custom domain
4. Update DNS records as instructed
5. Update `REDIRECT_URI` in backend and Google Console

---

## 🧪 Testing

### Local Development
```bash
cd webapp
python3 -m http.server 3000
# Visit: http://localhost:3000
```

### Vercel Development Server
```bash
vercel dev
# Visit: http://localhost:3000
```

### Production Test
After deployment:
```bash
curl https://your-app.vercel.app/api/env.js
# Should return: window.ENV_BACKEND_URL = "your-backend-url";
```

---

## 🔄 Update Process

### Update Environment Variables
```bash
# Update specific environment
vercel env add ENV_BACKEND_URL production

# Or via dashboard:
# Settings → Environment Variables → Edit
```

### Redeploy
```bash
# Latest changes
vercel --prod

# Or push to main branch (auto-deploys if connected to Git)
git push origin main
```

---

## 🐛 Troubleshooting

### Issue: "ENV_BACKEND_URL is undefined"

**Solution:**
1. Check environment variable is set in Vercel dashboard
2. Redeploy: `vercel --prod`
3. Clear browser cache

### Issue: "CORS error when calling backend"

**Solution:**
Update backend CORS settings to allow your Vercel domain:
```python
# backend/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: "OAuth redirect fails"

**Solution:**
1. Update redirect URI in Google Cloud Console
2. Add: `https://your-app.vercel.app/callback.html`
3. Update backend .env: `REDIRECT_URI=https://your-app.vercel.app/callback.html`

---

## 📊 Monitoring

Vercel provides built-in monitoring:

1. **Analytics:** Settings → Analytics
2. **Logs:** Deployments → Select deployment → Logs
3. **Serverless Function Logs:** Functions → Select function → Logs

---

## 💰 Pricing

Vercel Free Tier includes:
- ✅ Unlimited personal projects
- ✅ 100 GB bandwidth/month
- ✅ Serverless functions
- ✅ Automatic HTTPS
- ✅ Custom domains

Perfect for this project!

---

## 🔗 Related Documentation

- **Backend Deployment:** See main [DEPLOYMENT.md](../DEPLOYMENT.md)
- **Google OAuth Setup:** See [README.md](../README.md#setup-google-cloud-project)
- **Vercel Docs:** https://vercel.com/docs

---

## 🎯 Complete Deployment Checklist

- [ ] Backend deployed (Heroku/Railway/VPS)
- [ ] Backend URL obtained
- [ ] Vercel account created
- [ ] Webapp deployed to Vercel
- [ ] `ENV_BACKEND_URL` set in Vercel
- [ ] Google OAuth redirect URI updated
- [ ] Test OAuth flow end-to-end
- [ ] Custom domain configured (optional)
- [ ] Backend CORS updated with Vercel URL

---

## 🎉 Success!

Once deployed, your URLs will be:
- **Webapp:** `https://your-app.vercel.app`
- **OAuth Callback:** `https://your-app.vercel.app/callback.html`
- **Env API:** `https://your-app.vercel.app/api/env.js`

Share the webapp URL in your Telegram bot and you're live! 🚀