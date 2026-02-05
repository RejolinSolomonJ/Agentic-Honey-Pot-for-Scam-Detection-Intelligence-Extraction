import os
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks, Depends
from typing import Optional
from dotenv import load_dotenv

from models import IncomingMessage, AgentResponse
# We will import services later once they are created
# from services.detector import ScamDetector
# from services.agent import AgenticHoneypot
# from services.extractor import IntelligenceExtractor

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agentic Honey-Pot API")

# Configure CORS to allow all origins and headers (including x-api-key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Simple in-memory storage for demonstration/MVP
# In production, use a database (Redis/Postgres)
sessions = {}

API_KEY = os.getenv("API_KEY", "secret")  # Defaults to "secret" if not set in env

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/")
def health_check():
    return {"status": "running", "service": "Agentic Honey-Pot", "model": "gemini-2.0-flash"}

import requests
from services.detector import detect_scam
from services.agent import generate_agent_reply
from services.extractor import extract_intelligence_data
from models import FinalCallbackPayload, ExtractedIntelligence

async def send_callback(session_id: str, history: int, intelligence: ExtractedIntelligence, scam_detected: bool):
    """
    Sends the final result to the evaluation endpoint.
    """
    payload = FinalCallbackPayload(
        sessionId=session_id,
        scamDetected=scam_detected,
        totalMessagesExchanged=history,
        extractedIntelligence=intelligence,
        agentNotes="Automated agent engagement."
    )
    
    try:
        url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
        # In a real app, this should be async or use a proper HTTP client
        # For simplicity here using requests in a background thread or just directly if fast enough
        # But we are in async def, so requests is blocking. Ideally use httpx.
        # For this prototype, I'll just use requests inside the background task wrapper provided by FastAPI.
        response = requests.post(url, json=payload.dict(), timeout=5)
        print(f"Callback sent for {session_id}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send callback: {e}")

@app.post("/api/v1/message", response_model=AgentResponse)
async def handle_message(
    body: IncomingMessage, 
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    session_id = body.sessionId
    user_message = body.message.text
    
    print(f"Received message for session {session_id}: {user_message}")

    # 1. Detect Scam
    is_scam = detect_scam(user_message)
    print(f"Scam detected: {is_scam}")
    
    if not is_scam:
        # If not a scam, we might still reply if it's an ongoing conversation, 
        # but for this challenge, we only activate agent if scam intent is detected.
        # However, if conversationHistory is not empty, it implies we are already engaged?
        # The prompt says: "If scam intent is detected, the AI Agent is activated"
        # If the history is non-empty, we can assume we are already in engagement.
        if not body.conversationHistory:
            return AgentResponse(status="success", reply="This system is optimized for scam detection. No scam detected.")
    
    # 2. Activate Agent
    reply = generate_agent_reply(body.conversationHistory, user_message)
    
    # 3. Extract Intelligence
    # We pass the full history plus current message
    intelligence = extract_intelligence_data(body.conversationHistory, user_message)
    
    # 4. Schedule Callback
    # The requirement says "Once... Logic extraction is finished". 
    # We'll update the platform with the latest intelligence.
    total_messages = len(body.conversationHistory) + 2 # +1 for user msg, +1 for agent reply (approx)
    
    background_tasks.add_task(
        send_callback, 
        session_id, 
        total_messages, 
        intelligence, 
        True # We are treating it as scam if we are replying
    )
    
    return AgentResponse(status="success", reply=reply)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
