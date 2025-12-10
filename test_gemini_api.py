"""
Test Gemini API Key Loading
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).resolve().parent / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("✅ .env loaded")
else:
    print("❌ .env not found")

# Check API key
api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print(f"✅ GEMINI_API_KEY found!")
    print(f"   Length: {len(api_key)} characters")
    print(f"   First 10 chars: {api_key[:10]}...")
    print(f"   Last 10 chars: ...{api_key[-10:]}")
    
    # Test Gemini connection
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # List available models
        print("\n📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"   - {model.name}")
        
        # Use available model
        print("\n🤖 Testing Gemini API...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello from Gemini!' in one sentence")
        print(f"✅ Gemini Response: {response.text}")
        print("\n🎉 Gemini API is working!")
        
    except Exception as e:
        print(f"\n❌ Error testing Gemini: {e}")
else:
    print("❌ GEMINI_API_KEY not found in environment")
    print("\nPlease check:")
    print("1. .env file exists")
    print("2. GEMINI_API_KEY is set in .env")
    print("3. Format: GEMINI_API_KEY=your-key-here")
