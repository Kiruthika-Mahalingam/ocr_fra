#!/bin/bash
# Fix package conflicts

echo "Fixing package conflicts..."

# Uninstall conflicting packages
pip uninstall -y httpx openai groq

# Reinstall with compatible versions
pip install httpx==0.24.1
pip install openai==1.10.0
pip install groq==0.9.0

echo "Done! Restart the backend now."