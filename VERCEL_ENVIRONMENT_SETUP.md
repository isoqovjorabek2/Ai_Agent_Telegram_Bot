# 🔐 Vercel Environment Variables - Quick Reference

## 📝 What You Need to Add in Vercel

When deploying the webapp to Vercel, you need to configure **ONE** environment variable:

### Required Environment Variable:

```
Variable Name: BACKEND_URL
Variable Value: [Your Backend API URL]
```

## 🎯 Examples:

| Hosting Platform | Example Value |
|------------------|---------------|
| Heroku | `https://your-app.herokuapp.com` |
| Railway | `https://your-app.up.railway.app` |
| Render | `https://your-app.onrender.com` |
| Custom Domain | `https://api.yourdomain.com` |
| Local Development | `http://localhost:8000` |

**Important:** 
- ❌ Do NOT include trailing slash: `https://api.example.com/` (wrong)
- ✅ Correct format: `https://api.example.com` (right)

## 🚀 How to Add in Vercel

### Method 1: Vercel Dashboard

1. Go to your project in Vercel
2. Click **Settings**
3. Click **Environment Variables** in the sidebar
4. Click **Add New**
5. Fill in:
   - **Key**: `BACKEND_URL`
   - **Value**: Your backend URL (e.g., `https://your-app.herokuapp.com`)
   - **Environments**: Select all (Production, Preview, Development)
6. Click **Save**
7. Redeploy your project

### Method 2: Vercel CLI

```bash
# Login to Vercel
vercel login

# Add environment variable
vercel env add BACKEND_URL

# You'll be prompted to enter:
# - The value: https://your-backend-url.com
# - Which environments: a (all)

# Redeploy
vercel --prod
```

## ✅ Verification

After setting the environment variable:

1. **Check Build Logs**:
   - Go to your latest deployment in Vercel
   - Check the build logs
   - Look for: "✅ env.js generated successfully"
   - Verify it shows your BACKEND_URL

2. **Check Generated File**:
   - After deployment, your `env.js` should contain:
     ```javascript
     window.ENV_BACKEND_URL = "https://your-actual-backend-url.com";
     ```

3. **Test in Browser**:
   - Open your Vercel URL
   - Open browser console (F12)
   - You should see: `🔧 App Config: {BACKEND_URL: "https://..."}`

## 🔄 When to Update

Update `BACKEND_URL` when:
- ✅ You change backend hosting platforms
- ✅ You switch from dev to production backend
- ✅ Your backend URL changes
- ✅ You move to a custom domain

## 🐛 Troubleshooting

### Issue: "Failed to connect to backend"
**Check:**
1. Is `BACKEND_URL` set in Vercel? (Settings → Environment Variables)
2. Is the URL correct and accessible?
3. Did you redeploy after adding the variable?

**How to fix:**
```bash
# Verify environment variable is set
vercel env ls

# If not set, add it
vercel env add BACKEND_URL

# Redeploy
vercel --prod
```

### Issue: "BACKEND_URL is undefined" in console
**Check:**
1. Build script ran successfully
2. `env.js` was generated during build
3. `env.js` is loaded before `config.js` in HTML

**How to fix:**
- Check Vercel build logs
- Verify `vercel.json` has: `"buildCommand": "bash build-env.sh"`
- Ensure HTML files include: `<script src="env.js"></script>`

### Issue: CORS errors when calling backend
**This is NOT a Vercel issue** - fix in backend:

```python
# In your backend app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-project.vercel.app",  # Add your Vercel URL
        "http://localhost:3000"  # For local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📋 Complete Setup Checklist

- [ ] Backend is deployed and running
- [ ] Got backend URL (e.g., from Heroku dashboard)
- [ ] Webapp is deployed to Vercel
- [ ] `BACKEND_URL` environment variable added in Vercel
- [ ] Redeployed webapp after adding environment variable
- [ ] Tested webapp in browser
- [ ] Verified browser console shows correct BACKEND_URL
- [ ] Tested OAuth flow from Telegram bot
- [ ] OAuth completes successfully

## 🎓 Understanding the Flow

1. **During Build** (on Vercel):
   ```
   Vercel runs: bash build-env.sh
   ↓
   Script reads: $BACKEND_URL (from Vercel env vars)
   ↓
   Generates: env.js with window.ENV_BACKEND_URL
   ```

2. **During Runtime** (in browser):
   ```
   Browser loads: env.js
   ↓
   Sets: window.ENV_BACKEND_URL
   ↓
   config.js reads it
   ↓
   Creates: window.APP_CONFIG.BACKEND_URL
   ↓
   oauth.js uses it to make API calls
   ```

## 📚 Related Documentation

- **Full Deployment Guide**: `webapp/VERCEL_DEPLOYMENT.md`
- **All Environment Variables**: `ENVIRONMENT_VARIABLES.md`
- **Setup Complete**: `WEBAPP_SETUP_COMPLETE.md`
- **Deployment Summary**: `DEPLOYMENT_SUMMARY.md`

## 💡 Pro Tips

1. **Use Vercel Preview Deployments**:
   - Set different `BACKEND_URL` for preview vs production
   - Test changes before going live

2. **Custom Domains**:
   - You can use custom domains in Vercel
   - Remember to update Google OAuth URIs

3. **Environment-Specific Backends**:
   ```
   Production: BACKEND_URL=https://api.production.com
   Preview: BACKEND_URL=https://api.staging.com
   Development: BACKEND_URL=http://localhost:8000
   ```

4. **Security**:
   - Never expose backend API keys in frontend
   - `BACKEND_URL` is safe to expose (it's just a URL)
   - Keep sensitive keys in backend environment variables

## ✨ That's It!

You only need to set **ONE** environment variable in Vercel:
- `BACKEND_URL` = Your backend API URL

Everything else is handled automatically by the build script! 🎉

---

**Still stuck?** Check the troubleshooting section or review `webapp/VERCEL_DEPLOYMENT.md` for detailed step-by-step instructions.
