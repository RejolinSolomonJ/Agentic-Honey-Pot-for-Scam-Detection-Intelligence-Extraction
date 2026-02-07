import os
from .llm_wrapper import generate_content

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
        prompt = (
            "You are a Scam Detection AI. Analyze the user message. "
            "If it looks like a scam, phishing, or fraud attempt, reply exactly 'TRUE'. "
            "Otherwise, reply 'FALSE'.\n\n"
            f"Message: {text}"
        )
        
        # Use wrapper for generation
        content = generate_content(prompt).strip().upper()
        return "TRUE" in content
    except Exception as e:
        print(f"Error in detect_scam: {e}")
        # Fallback to keyword match if API fails
        return False
