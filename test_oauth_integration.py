#!/usr/bin/env python3
"""
Integration test for OAuth flow
This script tests the connection between frontend and backend for Google sign-in
"""

import os
import sys
import httpx
import json
from datetime import datetime

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def check_backend_health(backend_url):
    """Check if backend is running"""
    try:
        response = httpx.get(f"{backend_url}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is running: {data.get('service', 'unknown')}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cannot connect to backend: {e}")
        return False

def test_auth_initiate(backend_url, user_id):
    """Test OAuth initiation endpoint"""
    try:
        response = httpx.post(
            f"{backend_url}/api/auth/initiate",
            json={"user_id": user_id},
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'auth_url' in data:
                print_success("OAuth initiation endpoint works")
                print_info(f"Auth URL: {data['auth_url'][:100]}...")
                return True
            else:
                print_error("No auth_url in response")
                return False
        else:
            print_error(f"Auth initiate failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Auth initiate error: {e}")
        return False

def test_auth_status(backend_url, user_id):
    """Test auth status endpoint"""
    try:
        response = httpx.get(f"{backend_url}/api/auth/status/{user_id}")
        if response.status_code == 200:
            data = response.json()
            print_success("Auth status endpoint works")
            print_info(f"Authenticated: {data.get('authenticated', False)}")
            if data.get('authenticated'):
                print_info(f"Email: {data.get('email', 'N/A')}")
            return True
        else:
            print_error(f"Auth status failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Auth status error: {e}")
        return False

def test_database_init():
    """Test database initialization"""
    try:
        from backend.db import init_db
        init_db()
        print_success("Database initialized successfully")
        return True
    except Exception as e:
        print_error(f"Database init error: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = {
        'GOOGLE_CLIENT_ID': 'Google OAuth Client ID',
        'GOOGLE_CLIENT_SECRET': 'Google OAuth Client Secret',
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot Token'
    }
    
    optional_vars = {
        'WEBAPP_URL': 'Webapp URL',
        'REDIRECT_URI': 'OAuth Redirect URI',
        'BACKEND_URL': 'Backend URL'
    }
    
    all_good = True
    
    print_info("\nChecking required environment variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            masked = value[:10] + '...' if len(value) > 10 else value
            print_success(f"{var}: {masked} ({description})")
        else:
            print_error(f"{var} not set ({description})")
            all_good = False
    
    print_info("\nChecking optional environment variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print_success(f"{var}: {value} ({description})")
        else:
            print_warning(f"{var} not set ({description}) - using default")
    
    return all_good

def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}OAuth Integration Test{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    backend_url = os.getenv('BACKEND_URL', 'http://localhost:8000')
    test_user_id = 123456789  # Test user ID
    
    print_info(f"Testing backend at: {backend_url}")
    print_info(f"Test user ID: {test_user_id}\n")
    
    results = []
    
    # Test 1: Environment Variables
    print(f"\n{BLUE}Test 1: Environment Variables{RESET}")
    results.append(('Environment Variables', check_environment_variables()))
    
    # Test 2: Database Initialization
    print(f"\n{BLUE}Test 2: Database Initialization{RESET}")
    results.append(('Database Init', test_database_init()))
    
    # Test 3: Backend Health
    print(f"\n{BLUE}Test 3: Backend Health Check{RESET}")
    results.append(('Backend Health', check_backend_health(backend_url)))
    
    # Test 4: Auth Initiate
    print(f"\n{BLUE}Test 4: OAuth Initiation{RESET}")
    results.append(('OAuth Initiate', test_auth_initiate(backend_url, test_user_id)))
    
    # Test 5: Auth Status
    print(f"\n{BLUE}Test 5: Auth Status{RESET}")
    results.append(('Auth Status', test_auth_status(backend_url, test_user_id)))
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{BLUE}Result: {passed}/{total} tests passed{RESET}\n")
    
    if passed == total:
        print_success("All tests passed! Backend is ready for deployment.")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
