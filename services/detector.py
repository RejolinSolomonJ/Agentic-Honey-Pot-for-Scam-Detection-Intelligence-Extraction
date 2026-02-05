import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GRAPH_API_KEY = os.getenv("GEMINI_API_KEY")
if GRAPH_API_KEY:
    genai.configure(api_key=GRAPH_API_KEY)

def detect_scam(text: str) -> bool:
    """
    Analyzes the message to check for scam intent.
    Returns True if scam, False otherwise.
    """
    # Quick keyword check fallback
    scam_keywords = ["verify immediately", "account blocked", "urgent", "suspend", "kyc", "verify now", "blocked", "click here"]
    if any(k in text.lower() for k in scam_keywords):
        return True

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "You are a Scam Detection AI. Analyze the user message. "
            "If it looks like a scam, phishing, or fraud attempt, reply exactly 'TRUE'. "
            "Otherwise, reply 'FALSE'.\n\n"
            f"Message: {text}"
        )
        response = model.generate_content(prompt)
        content = response.text.strip().upper()
        return "TRUE" in content
    except Exception as e:
        print(f"Error in detect_scam: {e}")
        # Fallback to keyword match if API fails
        return False
