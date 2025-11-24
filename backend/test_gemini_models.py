

# # import google.generativeai as genai

# # genai.configure(api_key="AIzaSyDqdSIdQTWvhm5qYcTU_voicCxyzwZhfnU")

# # for m in genai.list_models(page_size=100):
# #     if "generateContent" in m.supported_generation_methods:
# #         print(m.name)



# import google.generativeai as genai

# genai.configure(api_key="AIzaSyDqdSIdQTWvhm5qYcTU_voicCxyzwZhfnU")

# models = genai.list_models()

# for m in models:
#     print(m.name)


"""
Quick Gemini API Test
Save as: test_gemini.py
Run: python test_gemini.py
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"✓ API Key loaded: {api_key[:15]}...{api_key[-5:]}")
print()

# Configure API
try:
    genai.configure(api_key=api_key)
    print("✓ Gemini API configured successfully")
    print()
except Exception as e:
    print(f"❌ Failed to configure API: {e}")
    exit(1)

# List all available models
print("=" * 70)
print("AVAILABLE MODELS WITH generateContent SUPPORT:")
print("=" * 70)

available_models = []
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"\n✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            if hasattr(model, 'description') and model.description:
                print(f"  Description: {model.description[:80]}...")
except Exception as e:
    print(f"❌ Error listing models: {e}")
    exit(1)

print("\n" + "=" * 70)
print(f"TOTAL MODELS FOUND: {len(available_models)}")
print("=" * 70)

# Test the first available model
if available_models:
    test_model_name = available_models[0]
    print(f"\n🧪 Testing model: {test_model_name}")
    print("-" * 70)
    
    try:
        model = genai.GenerativeModel(test_model_name)
        response = model.generate_content("Hello! Respond with 'API is working!'")
        print(f"✓ Model test SUCCESSFUL!")
        print(f"  Response: {response.text}")
        print()
    except Exception as e:
        print(f"❌ Model test FAILED: {e}")
        print()
        
    # Show code to use in GeminiService
    print("=" * 70)
    print("✅ COPY THIS INTO YOUR GeminiService __init__ METHOD:")
    print("=" * 70)
    print(f"""
    # In app/services/gemini_service.py, line ~15:
    self.model = genai.GenerativeModel("{test_model_name}")
    print("✓ Gemini service initialized with {test_model_name}")
    """)
    
    # Show all working models
    if len(available_models) > 1:
        print("\n📋 ALL WORKING MODEL NAMES:")
        for i, model_name in enumerate(available_models, 1):
            print(f"  {i}. {model_name}")
else:
    print("\n❌ No models found with generateContent support!")
    print("   Please check:")
    print("   1. API key is valid")
    print("   2. API key has Gemini API enabled")
    print("   3. You have quota remaining")