#!/bin/bash

# Setup script for Telegram Bot with Google Calendar & Keep Integration

set -e

echo "🚀 Setting up Telegram Bot..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your credentials"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - GOOGLE_CLIENT_ID"
    echo "   - GOOGLE_CLIENT_SECRET"
    exit 1
fi

# Initialize database
echo "💾 Initializing database..."
cd backend && python3 db.py && cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Start the backend: cd backend && uvicorn app:app --reload"
echo "3. Start the webapp: cd webapp && python3 -m http.server 3000"
echo "4. Start the bot: cd telegram-bot && python3 bot.py"
echo ""
echo "For production deployment, see README.md"