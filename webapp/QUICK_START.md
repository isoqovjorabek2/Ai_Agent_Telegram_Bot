# ⚡ Quick Start - Deploy in 5 Minutes

## 🎯 What You Need

**Just ONE environment variable for Vercel:**
```
BACKEND_URL = https://your-backend-url.com
```

## 🚀 Deploy Now

### Step 1: Go to Vercel (2 minutes)
1. Visit: https://vercel.com/new
2. Import your repository
3. **Set Root Directory to**: `webapp`
4. Click "Deploy"

### Step 2: Add Environment Variable (1 minute)
1. Go to: Project Settings → Environment Variables
2. Add:
   - **Name**: `BACKEND_URL`
   - **Value**: Your backend URL (e.g., `https://your-app.herokuapp.com`)
   - **Environment**: All (Production, Preview, Development)
3. Click "Save"

### Step 3: Redeploy (1 minute)
1. Go to Deployments tab
2. Click "..." on latest deployment
3. Click "Redeploy"

### Step 4: Update Backend (1 minute)
After getting your Vercel URL (e.g., `https://your-project.vercel.app`):

Update these backend environment variables:
```
WEBAPP_URL=https://your-project.vercel.app
REDIRECT_URI=https://your-project.vercel.app/callback.html
```

### Step 5: Update Google OAuth (1 minute)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. APIs & Services → Credentials → Edit OAuth Client
3. Add to **Authorized redirect URIs**:
   ```
   https://your-project.vercel.app/callback.html
   ```
4. Save

## ✅ Done! Test It

1. Open Telegram bot
2. Use authentication command
3. Should open your Vercel webapp
4. Click "Sign in with Google"
5. Complete OAuth
6. Success! 🎉

---

**Need more details?** See `VERCEL_DEPLOYMENT.md` or `VERCEL_ENVIRONMENT_SETUP.md`
