import os
import json
import google.generativeai as genai
from typing import List
from models import Message, ExtractedIntelligence
from dotenv import load_dotenv

load_dotenv()
GRAPH_API_KEY = os.getenv("GEMINI_API_KEY")
if GRAPH_API_KEY:
    genai.configure(api_key=GRAPH_API_KEY)

def extract_intelligence_data(history: List[Message], current_message: str) -> ExtractedIntelligence:
    """
    Analyzes the full conversation to extract bank accounts, UPIs, etc.
    """
    full_text = "\n".join([f"{msg.sender}: {msg.text}" for msg in history])
    full_text += f"\nscammer: {current_message}"

    prompt = """
    Analyze the following conversation and extract intelligence.
    Return a JSON object with these keys:
    - bankAccounts (list of strings)
    - upiIds (list of strings)
    - phishingLinks (list of strings)
    - phoneNumbers (list of strings)
    - suspiciousKeywords (list of strings)
    
    If nothing is found for a category, return empty list.
    Only extract explicit values found in the text.
    Output JSON only, no markdown.
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        response = model.generate_content(prompt + "\n\nConversation:\n" + full_text)
        text = response.text
        # Clean up markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        return ExtractedIntelligence(**data)
    except Exception as e:
        print(f"Error in extract_intelligence_data: {e}")
        return ExtractedIntelligence()
