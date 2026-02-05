import os
import google.generativeai as genai
from typing import List
from models import Message
from dotenv import load_dotenv

load_dotenv()
GRAPH_API_KEY = os.getenv("GEMINI_API_KEY")
if GRAPH_API_KEY:
    genai.configure(api_key=GRAPH_API_KEY)

SYSTEM_PROMPT = """
You are a naive, slightly confused application agent acting as a potential victim. 
You are interacting with a suspected scammer. 
Your goal is to keep the conversation going to extract more information (UPI IDs, Bank details, links) without revealing you are an AI.
Do NOT reveal you are a bot. 
Act like a regular person who is worried about their account or money.
Ask clarifying questions. 
If they ask for sensitive info, ask why it is needed or pretend to have trouble finding it, to make them reveal more details or alternative payment methods.
Keep responses short and human-like.
"""

def generate_agent_reply(history: List[Message], current_message: str) -> str:
    """
    Generates a reply to the scammer using Gemini.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Prepend system prompt to history for gemini-pro compliance
        chat_history = [{"role": "user", "parts": [SYSTEM_PROMPT]}, {"role": "model", "parts": ["Understood. I will act as the naive user."]}]
        
        for msg in history:
            role = "user" if msg.sender == "scammer" else "model"
            chat_history.append({"role": role, "parts": [msg.text]})
            
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(current_message)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_agent_reply: {e}")
        return f"I am confused, can you explain again? (Error: {str(e)})"
