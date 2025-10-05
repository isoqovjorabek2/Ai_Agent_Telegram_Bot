#!/usr/bin/env python3
"""
Test script to validate the setup before deployment
"""

import os
import sys
import json
from pathlib import Path


def test_env_file():
    """Check if .env file exists and has required variables"""
    print("🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("  ⚠️  .env file not found. Using .env.example as reference.")
        return False
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'BACKEND_URL',
        'WEBAPP_URL',
        'REDIRECT_URI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"  ❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("  ✅ All required environment variables found")
    return True


def test_python_files():
    """Compile all Python files to check for syntax errors"""
    print("\n🔍 Checking Python files...")
    
    py_files = []
    for root, dirs, files in os.walk('.'):
        # Skip venv and __pycache__
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git']]
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    
    errors = []
    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), py_file, 'exec')
        except SyntaxError as e:
            errors.append(f"{py_file}: {e}")
    
    if errors:
        print("  ❌ Syntax errors found:")
        for error in errors:
            print(f"     {error}")
        return False
    
    print(f"  ✅ All {len(py_files)} Python files compiled successfully")
    return True


def test_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'telegram',
        'google.auth',
        'googleapiclient',
        'httpx'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"  ⚠️  Missing packages: {', '.join(missing)}")
        print("     Run: pip install -r backend/requirements.txt")
        return False
    
    print("  ✅ All required packages installed")
    return True


def test_file_structure():
    """Check if all required files exist"""
    print("\n🔍 Checking file structure...")
    
    required_files = [
        'backend/app.py',
        'backend/auth.py',
        'backend/db.py',
        'backend/google_calendar.py',
        'backend/notes.py',
        'backend/requirements.txt',
        'telegram-bot/bot.py',
        'telegram-bot/handlers.py',
        'webapp/index.html',
        'webapp/oauth.js',
        'webapp/config.js',
        'webapp/callback.html',
        '.env.example',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("  ❌ Missing files:")
        for file in missing_files:
            print(f"     {file}")
        return False
    
    print("  ✅ All required files present")
    return True


def test_database_init():
    """Check if database can be initialized"""
    print("\n🔍 Testing database initialization...")
    
    try:
        sys.path.insert(0, 'backend')
        from db import init_db
        
        # Use a test database
        os.environ['DB_PATH'] = 'test_db.sqlite'
        init_db()
        
        # Clean up
        if os.path.exists('test_db.sqlite'):
            os.remove('test_db.sqlite')
        
        print("  ✅ Database initialization successful")
        return True
    except Exception as e:
        print(f"  ❌ Database initialization failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Running Setup Validation Tests")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_python_files,
        test_dependencies,
        test_database_init,
        test_env_file,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n✅ All tests passed! Your setup is ready for deployment.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())