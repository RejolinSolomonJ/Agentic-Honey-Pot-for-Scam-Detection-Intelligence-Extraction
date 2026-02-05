import os
import sys
import threading
import time
from pyngrok import ngrok
import uvicorn
from main import app

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give it a second to start
    time.sleep(2)
    
    try:
        # Open a tunnel on port 8080
        public_url = ngrok.connect(8080).public_url
        print("\n" + "="*50)
        print(f"✅ YOUR PUBLIC URL IS: {public_url}")
        print(f"👉 Enter this in 'Honeypot API Endpoint URL': {public_url}/api/v1/message")
        print(f"👉 Enter this in 'x-api-key': secret")
        print("="*50 + "\n")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        sys.exit(0)
