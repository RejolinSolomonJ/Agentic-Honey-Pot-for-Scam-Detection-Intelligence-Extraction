import sys
import os
from dotenv import load_dotenv

load_dotenv()

print(f"Python executable: {sys.executable}")

try:
    import openai
    print("✅ openai library is installed.")
except ImportError:
    print("❌ openai library is NOT installed.")

try:
    import google.generativeai as genai
    print("✅ google-generativeai library is installed.")
except ImportError:
    print("❌ google-generativeai library is NOT installed.")

gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if gemini_key:
    print("✅ GEMINI_API_KEY is present.")
else:
    print("❌ GEMINI_API_KEY is missing.")

if openai_key:
    print("✅ OPENAI_API_KEY is present.")
else:
    print("❌ OPENAI_API_KEY is missing.")

try:
    from services.llm_wrapper import generate_content
    print("✅ Successfully imported services.llm_wrapper")
except Exception as e:
    print(f"❌ Failed to import services.llm_wrapper: {e}")
