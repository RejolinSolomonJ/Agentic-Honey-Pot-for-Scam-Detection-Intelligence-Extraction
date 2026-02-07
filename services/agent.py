import os
from typing import List
from models import Message
from .llm_wrapper import generate_chat_response

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
    Generates a reply to the scammer using the LLM wrapper (Gemini -> OpenAI fallback).
    """
    try:
        # Convert history to format expected by wrapper if needed, 
        # but wrapper handles Message objects if we adjust it or we just pass Message objects 
        # and wrapper logic handles it? 
        # My wrapper expects object with .sender and .text attributes primarily for the loop.
        # So passing 'history' (List[Message]) directly is fine as the wrapper iterates and checks .sender.
        
        reply = generate_chat_response(history, current_message, system_prompt=SYSTEM_PROMPT)
        return reply
    except Exception as e:
        print(f"Error in generate_agent_reply: {e}")
        return f"I am confused, can you explain again?"
