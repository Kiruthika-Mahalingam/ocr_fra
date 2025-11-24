#!/usr/bin/env python3
"""
Troubleshooting script for FRA Digitization System
Run this to diagnose common issues
"""

import sys
import os

print("="*80)
print("FRA Digitization System - Troubleshooting")
print("="*80)

# Check Python version
print(f"\n1. Python Version: {sys.version}")
if sys.version_info < (3, 9):
    print("   ⚠️  WARNING: Python 3.9+ recommended")
else:
    print("   ✓ OK")

# Check required packages
print("\n2. Checking Required Packages:")
packages = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "psycopg2",
    "google.generativeai",
    "openai",
    "PIL",
    "pdf2image",
    "aiofiles",
    "gtts"
]

for package in packages:
    try:
        __import__(package.replace("-", "_"))
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} - NOT INSTALLED")
        print(f"      Run: pip install {package}")

# Check environment variables
print("\n3. Checking Environment Variables:")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "GEMINI_API_KEY",
        "OPENAI_API_KEY",
        "DATABASE_URL"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"   ✓ {var}: {masked}")
        else:
            print(f"   ✗ {var}: NOT SET")
            print(f"      Add to .env file")
            
except ImportError:
    print("   ✗ python-dotenv not installed")
    print("      Run: pip install python-dotenv")

# Check database connection
print("\n4. Checking Database Connection:")
try:
    import psycopg2
    db_url = os.getenv("DATABASE_URL", "")
    
    if "postgresql://" in db_url:
        # Parse connection string
        parts = db_url.replace("postgresql://", "").split("@")
        if len(parts) == 2:
            user_pass = parts[0].split(":")
            host_db = parts[1].split("/")
            
            print(f"   Host: {host_db[0].split(':')[0]}")
            print(f"   Database: {host_db[1] if len(host_db) > 1 else 'unknown'}")
            
            # Try to connect
            try:
                conn = psycopg2.connect(db_url)
                conn.close()
                print("   ✓ Connection successful")
            except Exception as e:
                print(f"   ✗ Connection failed: {e}")
        else:
            print("   ✗ Invalid DATABASE_URL format")
    else:
        print("   ✗ DATABASE_URL not set or invalid")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check file permissions
print("\n5. Checking File Permissions:")
dirs = ["uploads", "processed"]
for dir_name in dirs:
    if os.path.exists(dir_name):
        if os.access(dir_name, os.W_OK):
            print(f"   ✓ {dir_name}/ - writable")
        else:
            print(f"   ✗ {dir_name}/ - not writable")
    else:
        print(f"   ⚠️  {dir_name}/ - does not exist")
        print(f"      Run: mkdir -p {dir_name}")

# Test Gemini API
print("\n6. Testing Gemini API:")
try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
        print("   ✓ Gemini API configured")
        
        # Try a simple test
        try:
            response = model.generate_content("Say 'Hello'")
            print(f"   ✓ API test successful: {response.text[:50]}")
        except Exception as e:
            print(f"   ✗ API test failed: {e}")
    else:
        print("   ✗ GEMINI_API_KEY not set")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test OpenAI API
print("\n7. Testing OpenAI API:")
try:
    import openai
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        client = openai.OpenAI(api_key=api_key)
        print("   ✓ OpenAI API configured")
        
        # Try to list models (doesn't count against usage)
        try:
            models = client.models.list()
            print("   ✓ API connection successful")
        except Exception as e:
            print(f"   ✗ API test failed: {e}")
    else:
        print("   ✗ OPENAI_API_KEY not set")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*80)
print("Troubleshooting Complete!")
print("="*80)

# Recommendations
print("\nRecommendations:")
print("1. Fix any ✗ issues listed above")
print("2. Make sure PostgreSQL is running")
print("3. Check backend terminal for detailed error logs")
print("4. Visit http://localhost:8000/health for API health status")
print("5. Visit http://localhost:8000/docs for API documentation")
print("\nIf issues persist, check:")
print("- Backend logs in terminal")
print("- Browser console (F12) for frontend errors")
print("- Network tab in browser DevTools")