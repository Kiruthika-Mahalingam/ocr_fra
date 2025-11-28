#!/usr/bin/env python3
"""
Test OpenAI directly
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("Testing OpenAI Whisper")
print("="*80)

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"\n1. API Key: {api_key[:20]}...{api_key[-10:] if api_key else 'NOT SET'}")

# Try importing
print("\n2. Importing openai...")
try:
    import openai
    print(f"   ✓ openai version: {openai.__version__}")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    print("   Run: pip install openai==1.10.0")
    exit(1)

# Try initializing client
print("\n3. Initializing OpenAI client...")
try:
    client = openai.OpenAI(api_key=api_key)
    print("   ✓ Client created")
except Exception as e:
    print(f"   ✗ Client creation failed: {e}")
    exit(1)

# Try listing models (doesn't count against usage)
print("\n4. Testing API connection...")
try:
    models = client.models.list()
    print("   ✓ API connection successful")
    print(f"   Available models: {len(list(models))} models found")
except Exception as e:
    print(f"   ✗ API test failed: {e}")
    print("\nPossible issues:")
    print("  - Invalid API key")
    print("  - No internet connection")
    print("  - OpenAI API is down")
    print("  - API key doesn't have billing enabled")

print("\n" + "="*80)
print("Test Complete!")
print("="*80)