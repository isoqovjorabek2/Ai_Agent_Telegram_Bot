# Changelog

All notable changes, bug fixes, and improvements to this project.

## [1.1.0] - 2025-10-05 - Production Ready Release

### 🐛 Critical Bug Fixes

#### 1. OAuth Scope Issue (HIGH PRIORITY)
- **Issue**: Using invalid Google Keep API scope `https://www.googleapis.com/auth/keep`
- **Impact**: OAuth flow would fail because this scope doesn't exist
- **Fix**: Changed to `https://www.googleapis.com/auth/tasks` as Keep API is not publicly available
- **File**: `backend/auth.py` line 10-13

#### 2. Webapp OAuth Redirect Mismatch (HIGH PRIORITY)
- **Issue**: `webapp/oauth.js` was redirecting to `/auth/google?user_id=` endpoint that doesn't exist
- **Impact**: Sign-in flow would break completely
- **Fix**: Updated to use proper API endpoint `/api/auth/initiate`
- **Files**: `webapp/oauth.js` lines 25-61

#### 3. SQL Injection Vulnerability (SECURITY)
- **Issue**: Direct string interpolation in SQL query in `save_user_preference` function
- **Impact**: Potential SQL injection attack vector
- **Fix**: Added whitelist validation for preference keys
- **File**: `backend/db.py` lines 177-195

#### 4. Token Expiry Check Bug (MEDIUM PRIORITY)
- **Issue**: `creds.expired` check would fail if expiry is None
- **Impact**: Token refresh would crash, breaking authentication
- **Fix**: Added proper validation with `creds.valid` check
- **File**: `backend/auth.py` lines 102-115

#### 5. Indentation Error (SYNTAX)
- **Issue**: Incorrect indentation in bot.py error handler
- **Impact**: Code wouldn't run properly
- **Fix**: Fixed indentation to 4 spaces
- **File**: `telegram-bot/bot.py` lines 131-133

### ☁️ Vercel Serverless Integration (NEW)

#### Serverless Function for Environment Variables
- Created `/api/env.js` serverless function
- Dynamically injects `ENV_BACKEND_URL` from Vercel environment
- No hardcoded URLs in frontend
- Secure configuration via Vercel dashboard
- **Files**: `webapp/api/env.js`, `webapp/vercel.json`

#### Vercel Deployment Configuration
- Complete `vercel.json` configuration
- Package.json for Vercel project metadata
- .vercelignore for deployment optimization
- Comprehensive Vercel deployment guide
- **Files**: `webapp/vercel.json`, `webapp/package.json`, `webapp/README_VERCEL.md`

### ✨ New Features

#### 1. OAuth Callback Handler Page
- Added proper callback.html page for OAuth flow
- Beautiful UI with status messages
- Automatic error handling and user feedback
- **File**: `webapp/callback.html`

#### 2. Environment-Based Configuration
- Created `config.js` for webapp configuration
- Supports environment variables for production
- Easy to update for different deployment environments
- **File**: `webapp/config.js`

#### 3. Automated Setup Script
- `setup.sh` - One-command setup for local development
- Checks Python version, creates venv, installs dependencies
- Initializes database automatically
- **File**: `setup.sh`

#### 4. Validation Testing Script
- `test_setup.py` - Validates entire setup before deployment
- Checks file structure, Python syntax, dependencies
- Tests database initialization
- Verifies environment variables
- **File**: `test_setup.py`

### 📦 Deployment Improvements

#### 1. Docker Support
- Complete Dockerfile for containerization
- Docker Compose configuration for all services
- Volume mapping for persistent data
- **Files**: `Dockerfile`, `docker-compose.yml`

#### 2. Platform-Specific Configs
- Procfile for Heroku/Railway deployment
- runtime.txt for Python version specification
- Proper .gitignore for security
- **Files**: `Procfile`, `runtime.txt`, `.gitignore`

#### 3. Comprehensive Documentation
- **QUICKSTART.md** - 10-minute setup guide for beginners
- **DEPLOYMENT.md** - Detailed deployment instructions for:
  - Docker
  - Heroku
  - Railway
  - VPS (Ubuntu/Debian)
  - Vercel/Netlify (webapp)
- Production checklist and monitoring guide

#### 4. Environment Template
- Complete .env.example with all required variables
- Clear documentation for each variable
- Separate sections for development and production
- **File**: `.env.example`

### 🔧 Code Quality Improvements

#### 1. Requirements Consistency
- Fixed httpx version mismatch (0.25.2 → 0.25.1)
- Aligned all requirements.txt files
- Verified all imports match installed packages

#### 2. Error Handling
- Improved error messages in bot
- Better exception handling in auth flow
- Graceful degradation when backend is unavailable

#### 3. Security Enhancements
- Input validation on preference keys
- Proper token refresh error handling
- Secure credential storage practices documented

### 📝 Documentation Updates

#### Updated README.md
- Added quick start reference
- Added deployment guide reference
- Listed all bug fixes
- Added security notes section
- Updated features list with new capabilities

#### New Documentation Files
- QUICKSTART.md - Fast setup for new users
- DEPLOYMENT.md - Complete deployment guide
- CHANGELOG.md - This file!

### 🧪 Testing & Validation

- All Python files compile successfully
- Database initialization tested
- File structure validated
- OAuth flow tested end-to-end
- No syntax errors in codebase

### 📊 Files Changed

**Modified:**
- `backend/auth.py` - Fixed OAuth scope and token refresh
- `backend/db.py` - Fixed SQL injection vulnerability
- `telegram-bot/bot.py` - Fixed indentation error
- `webapp/oauth.js` - Fixed OAuth redirect flow
- `webapp/index.html` - Added config.js import
- `requirements.txt` - Fixed version consistency
- `webapp/requirements.txt` - Fixed version consistency
- `README.md` - Major documentation update

**Added:**
- `webapp/callback.html` - OAuth callback handler
- `webapp/config.js` - Configuration management
- `.env.example` - Environment template
- `.gitignore` - Git ignore rules
- `setup.sh` - Automated setup script
- `test_setup.py` - Validation script
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Multi-service orchestration
- `Procfile` - Platform deployment config
- `runtime.txt` - Python version specification
- `QUICKSTART.md` - Quick start guide
- `DEPLOYMENT.md` - Deployment guide
- `CHANGELOG.md` - This changelog

### 🚀 Upgrade Notes

If you're upgrading from a previous version:

1. **Update OAuth Scopes in Google Cloud Console:**
   - Remove: `https://www.googleapis.com/auth/keep`
   - Add: `https://www.googleapis.com/auth/tasks`

2. **Update Redirect URI:**
   - Change to: `http://localhost:3000/callback.html` (development)
   - Or your production callback URL

3. **Re-install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Users need to re-authenticate:**
   - Delete old tokens from database
   - Have users run `/auth` command again

### 🎯 Breaking Changes

- OAuth redirect flow changed - old links won't work
- Keep API replaced with Tasks API - notes go to Google Tasks now
- Callback URL format changed - update in Google Console

### 📈 Next Steps / Roadmap

Future improvements to consider:
- [ ] Add rate limiting middleware
- [ ] Implement webhook mode for bot (instead of polling)
- [ ] Add Redis for session storage
- [ ] Implement user preferences UI
- [ ] Add support for recurring events
- [ ] Multi-language support expansion
- [ ] Analytics and usage tracking
- [ ] Backup/restore functionality

---

## [1.0.0] - Original Release

Initial version with basic functionality:
- Telegram bot with Uzbek/Russian NLP
- Google Calendar integration
- Google Keep integration (attempted)
- Basic OAuth flow
- SQLite database

### Known Issues (Fixed in 1.1.0)
- OAuth scope invalid
- Webapp redirect broken
- SQL injection vulnerability
- Token refresh issues
- Various minor bugs