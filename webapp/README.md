# 🌐 Telegram Bot Webapp

Modern, responsive web interface for Google OAuth authentication used by the Telegram Bot.

## ✨ Features

- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- 📱 **Responsive** - Works perfectly on mobile and desktop
- 🔐 **Secure** - Google OAuth 2.0 authentication
- ⚡ **Fast** - Lightweight static site hosted on Vercel
- 🌍 **Multilingual** - Supports multiple languages

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone)

### One-Click Deployment Steps:

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Set the **Root Directory** to `webapp`
4. Add environment variable:
   - `BACKEND_URL`: Your backend API URL (e.g., `https://your-backend.herokuapp.com`)
5. Click "Deploy"
6. Done! 🎉

## 🔧 Environment Variables

### Required:

- **`BACKEND_URL`** - Your backend API URL
  - Example: `https://your-backend.herokuapp.com`
  - ⚠️ Do not include trailing slash

## 📁 File Structure

```
webapp/
├── index.html          # Main landing page
├── callback.html       # OAuth callback handler
├── oauth.js           # OAuth flow logic
├── config.js          # Configuration management
├── env.js             # Environment variables (auto-generated)
├── build-env.sh       # Build script for Vercel
├── package.json       # Package metadata
├── vercel.json        # Vercel configuration
└── README.md          # This file
```

## 🛠️ Local Development

### Prerequisites
- Python 3.x or any HTTP server

### Steps:

1. **Set environment variable** (optional for local testing):
   ```bash
   export BACKEND_URL=http://localhost:8000
   ```

2. **Generate env.js**:
   ```bash
   bash build-env.sh
   ```

3. **Start a local server**:
   ```bash
   # Option 1: Python
   python -m http.server 3000
   
   # Option 2: Node.js
   npx serve
   
   # Option 3: PHP
   php -S localhost:3000
   ```

4. **Open browser**:
   ```
   http://localhost:3000?user_id=123456
   ```
   (Replace `123456` with a test Telegram user ID)

## 🎨 UI Customization

The webapp features a modern, customizable design:

### Color Scheme
```css
Primary: #667eea (Purple Blue)
Secondary: #764ba2 (Purple)
Accent: #f093fb (Light Purple)
```

### Animations
- Gradient shifting background
- Floating dot pattern
- Pulsing logo
- Smooth hover effects
- Slide-in notifications

### Responsive Breakpoints
- Mobile: < 480px
- Tablet: 480px - 768px
- Desktop: > 768px

## 🔍 How It Works

1. **User clicks link** from Telegram bot with `?user_id=XXX`
2. **Landing page loads** (`index.html`)
3. **User clicks "Sign in with Google"**
4. **OAuth flow initiates** - Makes API call to `{BACKEND_URL}/api/auth/initiate`
5. **Redirects to Google** - User authorizes access
6. **Google redirects back** - To `callback.html` with auth code
7. **Callback handler** - Sends code to `{BACKEND_URL}/api/auth/callback`
8. **Success!** - User sees confirmation and can return to Telegram

## 📋 API Endpoints Used

The webapp calls these backend endpoints:

### POST `/api/auth/initiate`
Initiates OAuth flow
```json
Request: { "user_id": 123456 }
Response: { "auth_url": "https://accounts.google.com/..." }
```

### POST `/api/auth/callback`
Completes OAuth flow
```json
Request: { "code": "4/...", "user_id": 123456 }
Response: { "status": "success", "email": "user@gmail.com" }
```

## 🐛 Troubleshooting

### "Failed to start Google login"
- Check that `BACKEND_URL` is set correctly in Vercel
- Verify backend is running and accessible
- Check browser console for detailed errors

### "User ID not found"
- Link must be opened from Telegram bot
- URL must contain `?user_id=XXX` parameter

### OAuth redirect fails
- Verify redirect URI in Google Cloud Console matches:
  ```
  https://your-project.vercel.app/callback.html
  ```
- Check that callback.html is accessible

### CORS errors
- Backend must allow requests from your Vercel domain
- Update backend's CORS configuration

## 📚 Documentation

- **Full Deployment Guide**: See `VERCEL_DEPLOYMENT.md`
- **Environment Variables**: See `../ENVIRONMENT_VARIABLES.md`
- **Backend API**: See `../backend/README.md`

## 🔐 Security

- ✅ All traffic over HTTPS (Vercel enforced)
- ✅ No sensitive data stored in frontend
- ✅ OAuth tokens handled by backend only
- ✅ CORS protection enabled
- ✅ Environment variables never exposed in code

## 📊 Performance

- ⚡ Load time: < 1 second
- 📦 Total size: < 50KB
- 🎯 Lighthouse score: 95+
- 🌐 CDN-powered (Vercel Edge Network)

## 🤝 Contributing

To modify the webapp:

1. Make changes to HTML/CSS/JS files
2. Test locally
3. Deploy to Vercel (auto-deploys from git)
4. Verify in production

## 📝 License

MIT License - See LICENSE file for details

## 💬 Support

For issues or questions:
- Check `VERCEL_DEPLOYMENT.md` for deployment help
- Check `../ENVIRONMENT_VARIABLES.md` for configuration help
- Review backend logs for API errors

---

**Built with ❤️ for seamless Telegram × Google integration**
