# Telegram Bot Webapp - Vercel Serverless

OAuth authentication webapp for the Telegram Bot, powered by **Vercel serverless functions**.

## ✨ Features

- ☁️ **Vercel Serverless Functions** - Dynamic environment variables
- 🔐 **OAuth Flow** - Google authentication
- 📱 **Responsive Design** - Works on all devices
- 🌍 **Multilingual** - Uzbek & Russian support
- ⚡ **Fast Deployment** - Deploy in under 5 minutes

---

## 🚀 Quick Deploy to Vercel

```bash
# 1. Install Vercel CLI (if not installed)
npm install -g vercel

# 2. Deploy
vercel --prod

# 3. Add environment variable
vercel env add ENV_BACKEND_URL
# Enter your backend URL when prompted

# Done! ✅
```

Your app will be live at: `https://your-app.vercel.app`

---

## 📁 File Structure

```
webapp/
├── api/
│   └── env.js              # Serverless function for environment variables
├── index.html              # Main OAuth login page
├── callback.html           # OAuth callback handler
├── oauth.js                # OAuth logic
├── config.js               # Configuration management
├── vercel.json             # Vercel deployment config
├── package.json            # Project metadata
├── .vercelignore           # Files to ignore during deployment
├── README.md               # This file
└── README_VERCEL.md        # Detailed Vercel deployment guide
```

---

## 🔧 How It Works

### Serverless Function (`api/env.js`)

The webapp uses a Vercel serverless function to inject environment variables:

```javascript
// api/env.js
export default function handler(req, res) {
  const backendUrl = process.env.ENV_BACKEND_URL || "http://localhost:8000";
  res.send(`window.ENV_BACKEND_URL = "${backendUrl}";`);
}
```

### HTML Loading

```html
<!-- Load environment from serverless function -->
<script src="/api/env.js"></script>

<!-- Then load app -->
<script src="config.js"></script>
<script src="oauth.js"></script>
```

### Benefits

- ✅ No hardcoded URLs in frontend
- ✅ Configure via Vercel dashboard
- ✅ Different backends for dev/staging/prod
- ✅ Secure and professional
- ✅ Easy to update

---

## 🌐 Local Development

```bash
# Start local server
python3 -m http.server 3000

# Visit
open http://localhost:3000
```

**Note:** In local development, the serverless function won't run. The app will use the fallback URL `http://localhost:8000`.

To test with Vercel locally:
```bash
vercel dev
```

---

## ⚙️ Configuration

### Environment Variables (Set in Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV_BACKEND_URL` | Backend API URL | `https://api.example.com` |

### How to Set

**Via Vercel CLI:**
```bash
vercel env add ENV_BACKEND_URL
```

**Via Vercel Dashboard:**
1. Go to your project
2. Settings → Environment Variables
3. Add `ENV_BACKEND_URL` with your backend URL
4. Redeploy

---

## 🧪 Testing

### Test Serverless Function

```bash
curl https://your-app.vercel.app/api/env.js
```

Expected output:
```javascript
window.ENV_BACKEND_URL = "https://your-backend.com";
window.ENV_CONFIG_LOADED = true;
```

### Test in Browser

1. Open webapp
2. Press F12 (Developer Console)
3. Check:
```javascript
console.log(window.ENV_BACKEND_URL);
// Should output your backend URL
```

---

## 🔄 Update Backend URL

```bash
# Update via CLI
vercel env add ENV_BACKEND_URL production

# Or via dashboard (Settings → Environment Variables)
# Then redeploy:
vercel --prod
```

---

## 🐛 Troubleshooting

### "ENV_BACKEND_URL is undefined"

**Solution:**
1. Check environment variable is set in Vercel
2. Redeploy: `vercel --prod`
3. Clear browser cache

### CORS Error

**Solution:** Update backend CORS to allow your Vercel domain:
```python
# backend/app.py
allow_origins=["https://your-app.vercel.app"]
```

### OAuth Redirect Fails

**Solution:** Update redirect URI in:
1. Google Cloud Console
2. Backend `.env` file

New URI: `https://your-app.vercel.app/callback.html`

---

## 📚 Documentation

- **Quick Deploy:** This file
- **Detailed Guide:** [README_VERCEL.md](README_VERCEL.md)
- **Full Deployment:** [../DEPLOYMENT.md](../DEPLOYMENT.md)
- **Technical Details:** [../VERCEL_INTEGRATION.md](../VERCEL_INTEGRATION.md)

---

## 🎯 Next Steps

1. ✅ Deploy to Vercel
2. ✅ Set `ENV_BACKEND_URL`
3. ✅ Update Google OAuth redirect URI
4. ✅ Update backend CORS
5. ✅ Test OAuth flow
6. 🎉 Go live!

---

## 📞 Need Help?

- **Vercel Issues:** See [README_VERCEL.md](README_VERCEL.md)
- **Deployment Issues:** See [../DEPLOYMENT.md](../DEPLOYMENT.md)
- **Backend Setup:** See [../README.md](../README.md)

---

## ✅ Status

**Version:** 1.2.0  
**Status:** ✅ Production Ready  
**Deployment:** Vercel Serverless Functions  

🚀 Ready to deploy!