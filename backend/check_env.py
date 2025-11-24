#!/usr/bin/env python3
"""
Check environment variables
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("Checking Environment Variables")
print("="*80)

keys_to_check = [
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "OPENAI_API_KEY",
    "DATABASE_URL"
]

for key in keys_to_check:
    value = os.getenv(key)
    if value:
        # Mask the value
        if len(value) > 10:
            masked = value[:8] + "..." + value[-4:]
        else:
            masked = "***"
        print(f"✓ {key}: {masked}")
    else:
        print(f"✗ {key}: NOT SET")

print("\n" + "="*80)

# Show what needs to be set
missing = [key for key in keys_to_check if not os.getenv(key)]

if missing:
    print("\nMissing keys:")
    for key in missing:
        print(f"  - {key}")
    
    print("\nAdd to backend/.env file:")
    for key in missing:
        if key == "GROQ_API_KEY":
            print(f"  {key}=gsk_your_groq_key_from_console.groq.com")
        elif key == "OPENAI_API_KEY":
            print(f"  {key}=sk-proj-your_openai_key")
        else:
            print(f"  {key}=your_value_here")
else:
    print("\n✓ All required keys are set!")