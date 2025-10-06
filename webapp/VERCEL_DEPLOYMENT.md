# 🚀 Vercel Deployment Guide for Telegram Bot Webapp

This guide explains how to deploy the webapp to Vercel and configure the required environment variables.

## 📋 Prerequisites

- A Vercel account (sign up at https://vercel.com)
- Vercel CLI installed (optional): `npm i -g vercel`
- Your backend API deployed and accessible

## 🌐 Required Environment Variables

When deploying to Vercel, you **MUST** configure the following environment variable:

### 1. `BACKEND_URL` (Required)
- **Description**: The URL of your deployed backend API
- **Example**: `https://your-backend.herokuapp.com` or `https://api.yourdomain.com`
- **Purpose**: The webapp uses this to make API calls for OAuth and calendar operations

**Note**: Do NOT include a trailing slash in the BACKEND_URL.

## 📦 Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub/GitLab/Bitbucket**

2. **Import project to Vercel**:
   - Go to https://vercel.com/new
   - Click "Import Project"
   - Select your repository
   - Set the root directory to `webapp`

3. **Configure Build Settings**:
   - Framework Preset: `Other`
   - Root Directory: `webapp`
   - Build Command: `bash build-env.sh`
   - Output Directory: `.` (current directory)
   - Install Command: (leave empty or use default)

4. **Add Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add the following:
     ```
     Name: BACKEND_URL
     Value: https://your-backend-url.com
     Environment: Production, Preview, Development
     ```

5. **Deploy**:
   - Click "Deploy"
   - Wait for the build to complete
   - Your webapp will be live at `https://your-project.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Navigate to webapp directory**:
   ```bash
   cd webapp
   ```

3. **Login to Vercel**:
   ```bash
   vercel login
   ```

4. **Deploy**:
   ```bash
   vercel
   ```

5. **Set Environment Variables**:
   ```bash
   vercel env add BACKEND_URL
   ```
   Enter your backend URL when prompted.

6. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

## 🔧 Vercel Configuration

The `vercel.json` file in the webapp directory contains the deployment configuration:

```json
{
  "version": 2,
  "name": "telegram-bot-webapp",
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    },
    {
      "src": "*.js",
      "use": "@vercel/static"
    }
  ]
}
```

## ✅ Post-Deployment Checklist

After deploying to Vercel:

1. **Update Google OAuth Redirect URI**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Navigate to APIs & Services → Credentials
   - Edit your OAuth 2.0 Client ID
   - Add your Vercel URL to Authorized redirect URIs:
     ```
     https://your-project.vercel.app/callback.html
     ```

2. **Update Backend Configuration**:
   - Update your backend's `WEBAPP_URL` environment variable to point to your Vercel deployment:
     ```
     WEBAPP_URL=https://your-project.vercel.app
     ```
   - Update `REDIRECT_URI`:
     ```
     REDIRECT_URI=https://your-project.vercel.app/callback.html
     ```

3. **Test the OAuth Flow**:
   - Open your Telegram bot
   - Try the authentication process
   - Verify that you're redirected to your Vercel-hosted webapp
   - Complete the OAuth flow and ensure it works end-to-end

## 🐛 Troubleshooting

### Issue: "Failed to start Google login"
- **Solution**: Verify that `BACKEND_URL` environment variable is set correctly in Vercel
- Check browser console for specific error messages

### Issue: OAuth redirect doesn't work
- **Solution**: Make sure the redirect URI in Google Cloud Console matches exactly:
  ```
  https://your-project.vercel.app/callback.html
  ```

### Issue: CORS errors
- **Solution**: Update your backend's CORS configuration to allow requests from your Vercel domain:
  ```python
  allow_origins=["https://your-project.vercel.app"]
  ```

## 📱 Custom Domain (Optional)

To use a custom domain:

1. Go to your Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed by Vercel
5. Update all OAuth redirect URIs accordingly

## 🔐 Security Best Practices

1. **HTTPS Only**: Vercel provides HTTPS by default - always use it
2. **Environment Variables**: Never commit sensitive data to git
3. **CORS**: Configure backend to only allow your Vercel domain
4. **OAuth Scopes**: Request only the minimum required Google API scopes

## 📊 Monitoring

- View deployment logs in Vercel dashboard
- Set up Vercel Analytics for usage insights
- Monitor your backend API logs for errors

## 🎉 Success!

Once deployed, your webapp will be accessible at:
- **Production**: `https://your-project.vercel.app`
- **Preview**: Unique URL for each git branch/PR

Users can now authenticate with Google directly from your Telegram bot! 🚀
