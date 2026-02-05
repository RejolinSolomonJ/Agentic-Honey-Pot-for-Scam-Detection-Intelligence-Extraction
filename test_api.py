import requests
import json
import time

# Function to get current public URL
def get_public_url():
    try:
        with open("connection_info.txt", "r") as f:
            content = f.read()
            if "from " in content:
                return content.split("from ")[1].strip() + "/api/v1/message"
    except:
        return "http://localhost:8080/api/v1/message"
    return "http://localhost:8080/api/v1/message"

url = get_public_url()
print(f"[*] Target URL: {url}\n")

headers = {
    "x-api-key": "secret",
    "Content-Type": "application/json"
}

# Simulate a scammer sending a message
scam_message = {
    "sessionId": "test-session-user-1",
    "message": {
        "sender": "scammer",
        "text": "Your account 987654321 is BLOCKED due to suspicious activity. Verify immediately at http://secure-bank-verify.com/login to avoid suspension.",
        "timestamp": int(time.time() * 1000)
    },
    "conversationHistory": []
}

print(f"[>] Scammer says: \"{scam_message['message']['text']}\"")
print("[*] Sending to Honey-Pot Agent...\n")

try:
    response = requests.post(url, headers=headers, json=scam_message)
    
    if response.status_code == 200:
        data = response.json()
        print(f"[<] Agent replied: \"{data.get('reply', 'No reply')}\"")
        print(f"[+] Status: {data.get('status')}")
    else:
        print(f"[-] Error: {response.status_code} - {response.text}")

except Exception as e:
    print(f"[-] Connection Failed: {e}")

