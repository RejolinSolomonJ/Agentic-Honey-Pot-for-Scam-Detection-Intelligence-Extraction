import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_content(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    Generates content using Gemini, falling back to OpenAI if Gemini fails.
    """
    # Attempt Gemini first
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            # Check if response was blocked or empty
            if response.text:
                return response.text
        except Exception as e:
            print(f"Gemini API failed: {e}. Attempting fallback to OpenAI...")
    else:
        print("Gemini API Key not found. Attempting fallback to OpenAI...")

    # Fallback to OpenAI
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo", # or gpt-4o, using 3.5-turbo as fallback default
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API failed: {e}")
            raise Exception("All LLM providers failed.")
    else:
        raise Exception("OpenAI API Key not configured and Gemini failed/missing.")

def generate_chat_response(history: list, current_message: str, system_prompt: str = "") -> str:
    """
    Generates a chat response. 
    History is expected to be a list of objects with 'role' ('user'/'model'/'assistant') and 'parts'/'content'.
    """
    # Attempt Gemini
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            
            # Convert history to Gemini format if needed
            gemini_history = []
            if system_prompt:
                 gemini_history.append({"role": "user", "parts": [system_prompt]})
                 gemini_history.append({"role": "model", "parts": ["Understood."]})
            
            for msg in history:
                role = "user" if msg.sender == "scammer" else "model"
                gemini_history.append({"role": role, "parts": [msg.text]})
                
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(current_message)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini Chat failed: {e}. Attempting fallback to OpenAI...")

    # Fallback to OpenAI
    if openai_client:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            for msg in history:
                role = "user" if msg.sender == "scammer" else "assistant"
                messages.append({"role": role, "content": msg.text})
            
            messages.append({"role": "user", "content": current_message})

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI Chat failed: {e}")
            raise Exception("All LLM providers failed.")
            
    raise Exception("No LLM provider available.")
